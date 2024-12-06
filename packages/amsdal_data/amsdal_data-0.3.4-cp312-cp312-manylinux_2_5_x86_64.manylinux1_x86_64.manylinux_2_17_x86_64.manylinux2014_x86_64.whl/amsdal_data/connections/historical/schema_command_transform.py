import uuid
from collections import defaultdict
from copy import copy
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

import amsdal_glue as glue
from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.identifier import get_identifier

from amsdal_data.connections.constants import METADATA_KEY
from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SCHEMA_NAME_FIELD
from amsdal_data.connections.constants import SCHEMA_VERSION_FIELD
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.command_builder import format_historical_table_name
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager

if TYPE_CHECKING:
    from amsdal_data.connections.async_sqlite_historical import AsyncSqliteHistoricalConnection
    from amsdal_data.connections.postgresql_historical import AsyncPostgresHistoricalConnection
    from amsdal_data.connections.postgresql_historical import PostgresHistoricalConnection
    from amsdal_data.connections.sqlite_historical import SqliteHistoricalConnection

SchemaT = TypeVar('SchemaT', bound=glue.RegisterSchema | glue.DeleteSchema)


class SchemaCommandExecutor:
    def __init__(
        self,
        connection: Union['SqliteHistoricalConnection', 'PostgresHistoricalConnection'],
        schema_command: glue.SchemaCommand,
    ) -> None:
        self.connection = connection
        self.schema_command = copy(schema_command)
        self.schema_version_manager = HistoricalSchemaVersionManager()

    def execute(self) -> list[glue.Schema | None]:
        result: list[glue.Schema | None] = []
        items = self._transform_mutations()

        for _mutation in items:
            _result = self._execute_mutation(_mutation)
            result.extend(_result)

        return result

    def _transform_mutations(
        self,
    ) -> list[glue.RegisterSchema | glue.DeleteSchema]:
        result: list[glue.RegisterSchema | glue.DeleteSchema] = []
        # group by schema name and type
        grouped: dict[tuple[str, type[glue.SchemaMutation]], list[glue.SchemaMutation]] = defaultdict(list)

        _type: type[glue.SchemaMutation]

        for schema_mutation in self.schema_command.mutations:
            if schema_mutation.get_schema_reference().version == '':
                self.connection.run_schema_mutation(schema_mutation)
                continue

            if not isinstance(schema_mutation, glue.DeleteSchema) and issubclass(
                type(schema_mutation), glue.ChangeSchema
            ):
                _type = glue.ChangeSchema
            else:
                _type = type(schema_mutation)

            grouped[(schema_mutation.get_schema_name(), _type)].append(schema_mutation)

        # transform
        for (_schema_name, _mutation_type), _mutations in grouped.items():
            if _mutation_type is glue.ChangeSchema:
                result.append(self._transform_change_mutations_to_register(_mutations))  # type: ignore[arg-type]
                continue

            _mutation: glue.RegisterSchema | glue.DeleteSchema

            if _mutation_type is glue.DeleteSchema:
                self._check_single_mutation(_mutations)

                delete_mutation: glue.DeleteSchema = _mutations[0]  # type: ignore[assignment]
                _mutation = self._set_schema_version(delete_mutation, force_new_version=True)
            else:
                self._check_single_mutation(_mutations)

                register_mutation: glue.RegisterSchema = _mutations[0]  # type: ignore[assignment]
                register_mutation = self._exclude_unique_constraints(register_mutation)
                register_mutation = self._adjust_pk_constraints(register_mutation)
                register_mutation = self._adjust_to_historical_properties(register_mutation)
                _mutation = self._set_schema_version(register_mutation, force_new_version=True)

            result.append(_mutation)
        return result

    def _execute_mutation(
        self,
        mutation: glue.RegisterSchema | glue.DeleteSchema,
    ) -> list[glue.Schema | None]:
        result: list[glue.Schema | None] = []
        reference = mutation.get_schema_reference()

        if isinstance(mutation, glue.RegisterSchema):
            _mutation = copy(mutation)
            _mutation.schema.name = format_historical_table_name(
                reference.name,
                reference.version,
            )
            self.connection.run_schema_mutation(_mutation)
            result.append(mutation.schema)
        else:
            result.append(None)

        # Register last class version
        self.schema_version_manager.register_last_version(
            schema_name=reference.name,
            schema_version=reference.version,
        )

        return result

    def _transform_change_mutations_to_register(
        self,
        mutations: list[glue.ChangeSchema],
    ) -> glue.RegisterSchema:
        _mutation = mutations[0]
        _existing_schema = self._get_existing_schema(
            schema_name=_mutation.schema_reference.name,
            schema_version=_mutation.schema_reference.version,
        )
        _schema = copy(_existing_schema)

        for _mutation in mutations:
            if isinstance(_mutation, glue.RenameSchema):
                _schema.name = _mutation.new_schema_name
            elif isinstance(_mutation, glue.AddProperty):
                _schema.properties.append(_mutation.property)
            elif isinstance(_mutation, glue.DeleteProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.property_name:
                        del _schema.properties[_index]
                        break
            elif isinstance(_mutation, glue.RenameProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.old_name:
                        _property.name = _mutation.new_name
                        break
            elif isinstance(_mutation, glue.UpdateProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.property.name:
                        _schema.properties[_index] = _mutation.property
                        break
            elif isinstance(_mutation, glue.AddConstraint):
                if not _schema.constraints:
                    _schema.constraints = []

                _schema.constraints.append(_mutation.constraint)
            elif isinstance(_mutation, glue.DeleteConstraint):
                for _index, _constraint in enumerate(_schema.constraints or []):
                    if _constraint.name == _mutation.constraint_name:
                        if _schema.constraints:
                            del _schema.constraints[_index]
                        break
            elif isinstance(_mutation, glue.AddIndex):
                if not _schema.indexes:
                    _schema.indexes = []
                _schema.indexes.append(_mutation.index)
            elif isinstance(_mutation, glue.DeleteIndex):
                for _idx, _item in enumerate(_schema.indexes or []):
                    if _item.name == _mutation.index_name:
                        if _schema.indexes:
                            del _schema.indexes[_idx]
                        break
            else:
                msg = f'Unsupported mutation type: {type(_mutation)}'
                raise ValueError(msg)

        _create_mutation = glue.RegisterSchema(schema=_schema)
        _create_mutation = self._exclude_unique_constraints(_create_mutation)
        _create_mutation = self._adjust_pk_constraints(_create_mutation)
        _create_mutation = self._adjust_to_historical_properties(_create_mutation)
        _create_mutation = self._set_schema_version(_create_mutation, force_new_version=True)

        return _create_mutation

    def _get_existing_schema(
        self,
        schema_name: str,
        schema_version: glue.Version | Versions | str = glue.Version.LATEST,
    ) -> glue.Schema:
        _existing_schemas = self.connection.query_schema(
            filters=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_NAME_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema_name),
                ),
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_VERSION_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema_version),
                ),
            ),
        )

        if len(_existing_schemas) != 1:
            msg = f'SchemaCommandExecutor._get_existing_schema failed: Expected 1 schema, got {len(_existing_schemas)}'
            raise ValueError(msg)

        return _existing_schemas[0]

    @staticmethod
    def _check_single_mutation(mutations: list[glue.SchemaMutation]) -> None:
        if len(mutations) != 1:
            msg = f'SchemaCommandExecutor._check_single_mutation failed: Expected 1 mutation, got {len(mutations)}'
            raise ValueError(msg)

    @staticmethod
    def _adjust_to_historical_properties(mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        if mutation.schema.name in (
            TRANSACTION_TABLE,
            METADATA_TABLE,
            REFERENCE_TABLE,
        ):
            return mutation

        for idx, _property in enumerate(mutation.schema.properties):
            if _property.name == METADATA_KEY:
                del mutation.schema.properties[idx]
                break

        if not any(_property.name == SECONDARY_PARTITION_KEY for _property in mutation.schema.properties):
            mutation.schema.properties.append(
                glue.PropertySchema(
                    name=SECONDARY_PARTITION_KEY,
                    type=str,
                    required=True,
                ),
            )

            for constraint in mutation.schema.constraints or []:
                if isinstance(constraint, glue.PrimaryKeyConstraint):
                    constraint.fields.append(SECONDARY_PARTITION_KEY)
                    break
        return mutation

    def _set_schema_version(
        self,
        mutation: SchemaT,
        *,
        force_new_version: bool = False,
    ) -> SchemaT:
        schema_version = mutation.get_schema_reference().version

        if not schema_version:
            return mutation

        if schema_version == glue.Version.LATEST or force_new_version:
            schema_version = get_identifier()

        if isinstance(mutation, glue.DeleteSchema):
            mutation.schema_reference.version = schema_version
        elif isinstance(mutation, glue.RegisterSchema):
            mutation.schema.version = schema_version

        return mutation

    @staticmethod
    def _exclude_unique_constraints(mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        _schema = copy(mutation.schema)
        _schema.constraints = [
            _constraint
            for _constraint in (_schema.constraints or [])
            if not isinstance(_constraint, glue.UniqueConstraint)
        ]
        return glue.RegisterSchema(schema=_schema)

    @classmethod
    def _adjust_pk_constraints(cls, mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        _schema = copy(mutation.schema)

        for _constraint in _schema.constraints or []:
            cls._adjust_pk_constraint(_constraint)

        return glue.RegisterSchema(schema=_schema)

    @staticmethod
    def _adjust_pk_constraint(constraint: BaseConstraint) -> None:
        if isinstance(constraint, glue.PrimaryKeyConstraint):
            if '_x_' in constraint.name:
                constraint.name = constraint.name.rsplit('_x_', 1)[0]

            constraint.name += f'_x_{uuid.uuid4().hex[:8]}'


class AsyncSchemaCommandExecutor:
    def __init__(
        self,
        connection: Union['AsyncSqliteHistoricalConnection', 'AsyncPostgresHistoricalConnection'],
        schema_command: glue.SchemaCommand,
    ) -> None:
        self.connection = connection
        self.schema_command = copy(schema_command)
        self.schema_version_manager = AsyncHistoricalSchemaVersionManager()

    async def execute(self) -> list[glue.Schema | None]:
        result: list[glue.Schema | None] = []
        items = await self._transform_mutations()

        for _mutation in items:
            _result = await self._execute_mutation(_mutation)
            result.extend(_result)

        return result

    async def _transform_mutations(
        self,
    ) -> list[glue.RegisterSchema | glue.DeleteSchema]:
        result: list[glue.RegisterSchema | glue.DeleteSchema] = []
        # group by schema name and type
        grouped: dict[tuple[str, type[glue.SchemaMutation]], list[glue.SchemaMutation]] = defaultdict(list)

        _type: type[glue.SchemaMutation]

        for schema_mutation in self.schema_command.mutations:
            if schema_mutation.get_schema_reference().version == '':
                await self.connection.run_schema_mutation(schema_mutation)
                continue

            if not isinstance(schema_mutation, glue.DeleteSchema) and issubclass(
                type(schema_mutation), glue.ChangeSchema
            ):
                _type = glue.ChangeSchema
            else:
                _type = type(schema_mutation)

            grouped[(schema_mutation.get_schema_name(), _type)].append(schema_mutation)

        # transform
        for (_schema_name, _mutation_type), _mutations in grouped.items():
            if _mutation_type is glue.ChangeSchema:
                result.append(await self._transform_change_mutations_to_register(_mutations))  # type: ignore[arg-type]
                continue

            _mutation: glue.RegisterSchema | glue.DeleteSchema

            if _mutation_type is glue.DeleteSchema:
                self._check_single_mutation(_mutations)

                delete_mutation: glue.DeleteSchema = _mutations[0]  # type: ignore[assignment]
                _mutation = self._set_schema_version(delete_mutation, force_new_version=True)
            else:
                self._check_single_mutation(_mutations)

                register_mutation: glue.RegisterSchema = _mutations[0]  # type: ignore[assignment]
                register_mutation = self._exclude_unique_constraints(register_mutation)
                register_mutation = self._adjust_pk_constraints(register_mutation)
                register_mutation = self._adjust_to_historical_properties(register_mutation)
                _mutation = self._set_schema_version(register_mutation, force_new_version=True)

            result.append(_mutation)
        return result

    async def _execute_mutation(
        self,
        mutation: glue.RegisterSchema | glue.DeleteSchema,
    ) -> list[glue.Schema | None]:
        result: list[glue.Schema | None] = []
        reference = mutation.get_schema_reference()

        if isinstance(mutation, glue.RegisterSchema):
            _mutation = copy(mutation)
            _mutation.schema.name = format_historical_table_name(
                reference.name,
                reference.version,
            )
            await self.connection.run_schema_mutation(_mutation)
            result.append(mutation.schema)
        else:
            result.append(None)

        # Register last class version
        self.schema_version_manager.register_last_version(
            schema_name=reference.name,
            schema_version=reference.version,
        )

        return result

    async def _transform_change_mutations_to_register(
        self,
        mutations: list[glue.ChangeSchema],
    ) -> glue.RegisterSchema:
        _mutation = mutations[0]
        _existing_schema = await self._get_existing_schema(
            schema_name=_mutation.schema_reference.name,
            schema_version=_mutation.schema_reference.version,
        )
        _schema = copy(_existing_schema)

        for _mutation in mutations:
            if isinstance(_mutation, glue.RenameSchema):
                _schema.name = _mutation.new_schema_name
            elif isinstance(_mutation, glue.AddProperty):
                _schema.properties.append(_mutation.property)
            elif isinstance(_mutation, glue.DeleteProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.property_name:
                        del _schema.properties[_index]
                        break
            elif isinstance(_mutation, glue.RenameProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.old_name:
                        _property.name = _mutation.new_name
                        break
            elif isinstance(_mutation, glue.UpdateProperty):
                for _index, _property in enumerate(_schema.properties):
                    if _property.name == _mutation.property.name:
                        _schema.properties[_index] = _mutation.property
                        break
            elif isinstance(_mutation, glue.AddConstraint):
                if not _schema.constraints:
                    _schema.constraints = []

                _schema.constraints.append(_mutation.constraint)
            elif isinstance(_mutation, glue.DeleteConstraint):
                for _index, _constraint in enumerate(_schema.constraints or []):
                    if _constraint.name == _mutation.constraint_name:
                        if _schema.constraints:
                            del _schema.constraints[_index]
                        break
            elif isinstance(_mutation, glue.AddIndex):
                if not _schema.indexes:
                    _schema.indexes = []
                _schema.indexes.append(_mutation.index)
            elif isinstance(_mutation, glue.DeleteIndex):
                for _idx, _item in enumerate(_schema.indexes or []):
                    if _item.name == _mutation.index_name:
                        if _schema.indexes:
                            del _schema.indexes[_idx]
                        break
            else:
                msg = f'Unsupported mutation type: {type(_mutation)}'
                raise ValueError(msg)

        _create_mutation = glue.RegisterSchema(schema=_schema)
        _create_mutation = self._exclude_unique_constraints(_create_mutation)
        _create_mutation = self._adjust_pk_constraints(_create_mutation)
        _create_mutation = self._adjust_to_historical_properties(_create_mutation)
        _create_mutation = self._set_schema_version(_create_mutation, force_new_version=True)

        return _create_mutation

    async def _get_existing_schema(
        self,
        schema_name: str,
        schema_version: glue.Version | Versions | str = glue.Version.LATEST,
    ) -> glue.Schema:
        _existing_schemas = await self.connection.query_schema(
            filters=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_NAME_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema_name),
                ),
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_VERSION_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema_version),
                ),
            ),
        )

        if len(_existing_schemas) != 1:
            msg = f'SchemaCommandExecutor._get_existing_schema failed: Expected 1 schema, got {len(_existing_schemas)}'
            raise ValueError(msg)

        return _existing_schemas[0]

    @staticmethod
    def _check_single_mutation(mutations: list[glue.SchemaMutation]) -> None:
        if len(mutations) != 1:
            msg = f'SchemaCommandExecutor._check_single_mutation failed: Expected 1 mutation, got {len(mutations)}'
            raise ValueError(msg)

    @staticmethod
    def _adjust_to_historical_properties(mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        if mutation.schema.name in (
            TRANSACTION_TABLE,
            METADATA_TABLE,
            REFERENCE_TABLE,
        ):
            return mutation

        for idx, _property in enumerate(mutation.schema.properties):
            if _property.name == METADATA_KEY:
                del mutation.schema.properties[idx]
                break

        if not any(_property.name == SECONDARY_PARTITION_KEY for _property in mutation.schema.properties):
            mutation.schema.properties.append(
                glue.PropertySchema(
                    name=SECONDARY_PARTITION_KEY,
                    type=str,
                    required=True,
                ),
            )

            for constraint in mutation.schema.constraints or []:
                if isinstance(constraint, glue.PrimaryKeyConstraint):
                    constraint.fields.append(SECONDARY_PARTITION_KEY)
                    break
        return mutation

    def _set_schema_version(
        self,
        mutation: SchemaT,
        *,
        force_new_version: bool = False,
    ) -> SchemaT:
        schema_version = mutation.get_schema_reference().version

        if not schema_version:
            return mutation

        if schema_version == glue.Version.LATEST or force_new_version:
            schema_version = get_identifier()

        if isinstance(mutation, glue.DeleteSchema):
            mutation.schema_reference.version = schema_version
        elif isinstance(mutation, glue.RegisterSchema):
            mutation.schema.version = schema_version

        return mutation

    @staticmethod
    def _exclude_unique_constraints(mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        _schema = copy(mutation.schema)
        _schema.constraints = [
            _constraint
            for _constraint in (_schema.constraints or [])
            if not isinstance(_constraint, glue.UniqueConstraint)
        ]
        return glue.RegisterSchema(schema=_schema)

    @classmethod
    def _adjust_pk_constraints(cls, mutation: glue.RegisterSchema) -> glue.RegisterSchema:
        _schema = copy(mutation.schema)

        for _constraint in _schema.constraints or []:
            cls._adjust_pk_constraint(_constraint)

        return glue.RegisterSchema(schema=_schema)

    @staticmethod
    def _adjust_pk_constraint(constraint: BaseConstraint) -> None:
        if isinstance(constraint, glue.PrimaryKeyConstraint):
            if '_x_' in constraint.name:
                constraint.name = constraint.name.rsplit('_x_', 1)[0]

            constraint.name += f'_x_{uuid.uuid4().hex[:8]}'
