import os
from collections.abc import AsyncGenerator
from collections.abc import Generator
from typing import Any

import amsdal_glue as glue
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.utils.singleton import Singleton

from amsdal_data.aliases.using import LAKEHOUSE_DB_ALIAS
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.historical.data_query_transform import METADATA_FIELD
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.errors import CommandError
from amsdal_data.errors import QueryError
from amsdal_data.errors import RegisterTableError
from amsdal_data.transactions.manager import AmsdalAsyncTransactionManager
from amsdal_data.transactions.manager import AmsdalTransactionManager

MIGRATION_BATCH_SIZE = int(os.getenv('AMSDAL_MIGRATION_BATCH_SIZE', 1000))  # noqa: PLW1508


class TableSchemasManager(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_data.application import DataApplication

        self._operation_manager = DataApplication().operation_manager

    def register_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        """
        Creates a new table in the database through connection.
        """
        existing_schema = self._get_existing_schema(schema, using=using)

        if existing_schema:
            self._update_table(schema, existing_schema, using=using)
        else:
            self._create_table(schema, using=using)

    def unregister_table(
        self,
        address: Address,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=address.class_name, version=address.class_version)

        if using == LAKEHOUSE_DB_ALIAS:
            result = self._operation_manager.perform_schema_command_lakehouse(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalTransactionManager().transaction_id,
                ),
            )
        else:
            result = self._operation_manager.perform_schema_command(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalTransactionManager().transaction_id,
                ),
            )

        if not result.success:
            msg = f'Failed to unregister schema: {result.message}'
            raise RegisterTableError(msg) from result.exception

    def _get_existing_schema(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> glue.Schema | None:
        if using == LAKEHOUSE_DB_ALIAS:
            _query = self._operation_manager.schema_query_lakehouse
        else:
            _query = self._operation_manager.schema_query

        result = _query(
            filters=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='name'), table_name='amsdal_schema_registry'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema.name),
                ),
            ),
        )

        if result.success:
            return result.schemas[0] if result.schemas else None

        msg = f'Error while getting schema {schema.name}: {result.message}'
        raise RegisterTableError(msg) from result.exception

    def _create_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = _command(
            glue.SchemaCommand(
                root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalTransactionManager().transaction_id,
                mutations=[
                    glue.RegisterSchema(schema=schema),
                ],
            ),
        )

        if not result.success:
            msg = f'Error while creating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception

    def _update_table(
        self,
        schema: glue.Schema,
        existing_schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=schema.name, version=existing_schema.version)
        mutations: list[glue.SchemaMutation] = []
        new_property_names = [_prop.name for _prop in schema.properties]
        existing_property_names = [existing_prop.name for existing_prop in existing_schema.properties]

        for existing_prop in existing_schema.properties:
            if existing_prop.name not in new_property_names:
                mutations.append(
                    glue.DeleteProperty(schema_reference=schema_reference, property_name=existing_prop.name)
                )
                continue

            new_prop = schema.properties[new_property_names.index(existing_prop.name)]

            # it's all the JSON field
            if existing_prop.type is list:
                existing_prop.type = dict

            if new_prop.type is list:
                new_prop.type = dict

            if existing_prop != new_prop:
                mutations.append(glue.UpdateProperty(schema_reference=schema_reference, property=new_prop))

        for new_prop in schema.properties:
            if new_prop.name not in existing_property_names:
                mutations.append(glue.AddProperty(schema_reference=schema_reference, property=new_prop))

        new_index_names = [index.name for index in schema.indexes or []]
        existing_index_names = [existing_index.name for existing_index in existing_schema.indexes or []]

        for existing_index in existing_schema.indexes or []:
            if existing_index.name not in new_index_names:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                continue

            new_index = (schema.indexes or [])[new_index_names.index(existing_index.name)]

            if existing_index != new_index:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        for new_index in schema.indexes or []:
            if new_index.name not in existing_index_names:
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        new_constraint_names = [constraint.name for constraint in schema.constraints or []]
        existing_constraint_names = [
            existing_constraint.name for existing_constraint in existing_schema.constraints or []
        ]

        for existing_constraint in existing_schema.constraints or []:
            if existing_constraint.name not in new_constraint_names:
                mutations.append(
                    glue.DeleteConstraint(schema_reference=schema_reference, constraint_name=existing_constraint.name)
                )
                continue

            new_constraint = (schema.constraints or [])[new_constraint_names.index(existing_constraint.name)]

            if existing_constraint != new_constraint:
                mutations.append(
                    glue.DeleteConstraint(
                        schema_reference=schema_reference,
                        constraint_name=existing_constraint.name,
                    ),
                )
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        for new_constraint in schema.constraints or []:
            if new_constraint.name not in existing_constraint_names:
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        if not mutations:
            return

        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = _command(
            glue.SchemaCommand(
                mutations=mutations,
                root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalTransactionManager().transaction_id,
            ),
        )

        if not result.success:
            msg = f'Error while updating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception

    def fetch_historical_data(
        self,
        schema_reference: glue.SchemaReference,
        batch_size: int = MIGRATION_BATCH_SIZE,
        offset: int = 0,
    ) -> Generator[dict[str, Any], None, None]:
        is_deleted_field = glue.FieldReference(
            field=glue.Field(
                name=METADATA_FIELD,
                child=glue.Field(name='is_deleted'),
            ),
            table_name=schema_reference.name,
        )
        is_deleted_field.field.child.parent = is_deleted_field.field  # type: ignore[union-attr]
        query = glue.QueryStatement(
            table=schema_reference,
            where=glue.Conditions(
                glue.Condition(
                    field=is_deleted_field,
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=False),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
            limit=glue.LimitQuery(limit=batch_size, offset=offset),
            order_by=[
                glue.OrderByQuery(
                    field=glue.FieldReference(
                        field=glue.Field(name='updated_at'),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    direction=glue.OrderDirection.ASC,
                ),
            ],
        )

        result = self._operation_manager.query_lakehouse(statement=query)

        if not result.success:
            msg = f'Error while fetching historical data: {result.message}'
            raise QueryError(msg) from result.exception

        for data in result.data or []:
            yield data.data

        if len(result.data or []) == batch_size:
            yield from self.fetch_historical_data(schema_reference, batch_size, offset + batch_size)

    def search_latest_class_object(
        self,
        schema_reference: glue.SchemaReference,
        class_object_name: str,
    ) -> dict[str, Any] | None:
        _conditions = [
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=PRIMARY_PARTITION_KEY),
                    table_name=schema_reference.name,
                ),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(class_object_name),
            ),
            glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(value=True),
                ),
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=''),
                ),
                connector=glue.FilterConnector.OR,
            ),
        ]

        result = self._operation_manager.query_lakehouse(
            statement=glue.QueryStatement(
                table=schema_reference,
                where=glue.Conditions(*_conditions),
                limit=glue.LimitQuery(limit=1),
            ),
        )

        if not result.success:
            msg = f'Error while searching latest class object version in lakehouse: {result.message}'
            raise QueryError(msg) from result.exception

        if result.data:
            return result.data[0].data
        return None

    def insert_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_data: glue.Data,
    ) -> dict[str, Any]:
        mutation = glue.InsertData(
            schema=schema_reference,
            data=[class_object_data],
        )

        return self._mutate_class_object_schema(mutation)

    def update_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_data: glue.Data,
    ) -> dict[str, Any]:
        next_version_field = glue.FieldReference(
            field=glue.Field(name=NEXT_VERSION_FIELD),
            table_name=METADATA_TABLE_ALIAS,
        )
        mutation = glue.UpdateData(
            schema=schema_reference,
            data=class_object_data,
            query=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                        table_name=schema_reference.name,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=class_object_data.data[PRIMARY_PARTITION_KEY]),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
        )

        return self._mutate_class_object_schema(mutation)

    def delete_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_id: str,
    ) -> dict[str, Any]:
        next_version_field = glue.FieldReference(
            field=glue.Field(name=NEXT_VERSION_FIELD),
            table_name=METADATA_TABLE_ALIAS,
        )
        mutation = glue.DeleteData(
            schema=schema_reference,
            query=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                        table_name=schema_reference.name,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=class_object_id),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
        )

        return self._mutate_class_object_schema(mutation)

    def _mutate_class_object_schema(
        self,
        mutation: glue.InsertData | glue.UpdateData | glue.DeleteData,
    ) -> dict[str, Any]:
        result = self._operation_manager.perform_data_command_lakehouse(
            command=glue.DataCommand(
                mutations=[mutation],
                root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalTransactionManager().transaction_id,
            ),
        )

        if not result.success:
            msg = f'Error while {mutation.__class__} class object schema in lakehouse: {result.message}'
            raise CommandError(msg) from result.exception

        # the first index 0 represents index of mutation, the second index - index of data
        return result.data[0][0].data  # type: ignore[index]


class AsyncTableSchemasManager(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_data.application import AsyncDataApplication

        self._operation_manager = AsyncDataApplication().operation_manager

    async def register_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        """
        Creates a new table in the database through connection.
        """
        existing_schema = await self._get_existing_schema(schema, using=using)

        if existing_schema:
            await self._update_table(schema, existing_schema, using=using)
        else:
            await self._create_table(schema, using=using)

    async def unregister_table(
        self,
        address: Address,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=address.class_name, version=address.class_version)

        if using == LAKEHOUSE_DB_ALIAS:
            result = await self._operation_manager.perform_schema_command_lakehouse(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalAsyncTransactionManager().transaction_id,
                ),
            )
        else:
            result = await self._operation_manager.perform_schema_command(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalAsyncTransactionManager().transaction_id,
                ),
            )

        if not result.success:
            msg = f'Failed to unregister schema: {result.message}'
            raise RegisterTableError(msg) from result.exception

    async def _get_existing_schema(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> glue.Schema | None:
        if using == LAKEHOUSE_DB_ALIAS:
            _query = self._operation_manager.schema_query_lakehouse
        else:
            _query = self._operation_manager.schema_query

        result = await _query(
            filters=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='name'), table_name='amsdal_schema_registry'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema.name),
                ),
            ),
        )

        if result.success:
            return result.schemas[0] if result.schemas else None

        msg = f'Error while getting schema {schema.name}: {result.message}'
        raise RegisterTableError(msg) from result.exception

    async def _create_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = await _command(
            glue.SchemaCommand(
                root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalAsyncTransactionManager().transaction_id,
                mutations=[
                    glue.RegisterSchema(schema=schema),
                ],
            ),
        )

        if not result.success:
            msg = f'Error while creating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception

    async def _update_table(
        self,
        schema: glue.Schema,
        existing_schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=schema.name, version=existing_schema.version)
        mutations: list[glue.SchemaMutation] = []
        new_property_names = [_prop.name for _prop in schema.properties]
        existing_property_names = [existing_prop.name for existing_prop in existing_schema.properties]

        for existing_prop in existing_schema.properties:
            if existing_prop.name not in new_property_names:
                mutations.append(
                    glue.DeleteProperty(schema_reference=schema_reference, property_name=existing_prop.name)
                )
                continue

            new_prop = schema.properties[new_property_names.index(existing_prop.name)]

            # it's all the JSON field
            if existing_prop.type is list:
                existing_prop.type = dict

            if new_prop.type is list:
                new_prop.type = dict

            if existing_prop != new_prop:
                mutations.append(glue.UpdateProperty(schema_reference=schema_reference, property=new_prop))

        for new_prop in schema.properties:
            if new_prop.name not in existing_property_names:
                mutations.append(glue.AddProperty(schema_reference=schema_reference, property=new_prop))

        new_index_names = [index.name for index in schema.indexes or []]
        existing_index_names = [existing_index.name for existing_index in existing_schema.indexes or []]

        for existing_index in existing_schema.indexes or []:
            if existing_index.name not in new_index_names:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                continue

            new_index = (schema.indexes or [])[new_index_names.index(existing_index.name)]

            if existing_index != new_index:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        for new_index in schema.indexes or []:
            if new_index.name not in existing_index_names:
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        new_constraint_names = [constraint.name for constraint in schema.constraints or []]
        existing_constraint_names = [
            existing_constraint.name for existing_constraint in existing_schema.constraints or []
        ]

        for existing_constraint in existing_schema.constraints or []:
            if existing_constraint.name not in new_constraint_names:
                mutations.append(
                    glue.DeleteConstraint(schema_reference=schema_reference, constraint_name=existing_constraint.name)
                )
                continue

            new_constraint = (schema.constraints or [])[new_constraint_names.index(existing_constraint.name)]

            if existing_constraint != new_constraint:
                mutations.append(
                    glue.DeleteConstraint(
                        schema_reference=schema_reference,
                        constraint_name=existing_constraint.name,
                    ),
                )
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        for new_constraint in schema.constraints or []:
            if new_constraint.name not in existing_constraint_names:
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        if not mutations:
            return

        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = await _command(
            glue.SchemaCommand(
                mutations=mutations,
                root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalAsyncTransactionManager().transaction_id,
            ),
        )

        if not result.success:
            msg = f'Error while updating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception

    async def insert_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_data: glue.Data,
    ) -> dict[str, Any]:
        mutation = glue.InsertData(
            schema=schema_reference,
            data=[class_object_data],
        )

        return await self._mutate_class_object_schema(mutation)

    async def update_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_data: glue.Data,
    ) -> dict[str, Any]:
        next_version_field = glue.FieldReference(
            field=glue.Field(name=NEXT_VERSION_FIELD),
            table_name=METADATA_TABLE_ALIAS,
        )
        mutation = glue.UpdateData(
            schema=schema_reference,
            data=class_object_data,
            query=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                        table_name=schema_reference.name,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=class_object_data.data[PRIMARY_PARTITION_KEY]),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
        )

        return await self._mutate_class_object_schema(mutation)

    async def delete_class_object_schema(
        self,
        schema_reference: glue.SchemaReference,
        class_object_id: str,
    ) -> dict[str, Any]:
        next_version_field = glue.FieldReference(
            field=glue.Field(name=NEXT_VERSION_FIELD),
            table_name=METADATA_TABLE_ALIAS,
        )
        mutation = glue.DeleteData(
            schema=schema_reference,
            query=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                        table_name=schema_reference.name,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=class_object_id),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=next_version_field,
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
        )

        return await self._mutate_class_object_schema(mutation)

    async def _mutate_class_object_schema(
        self,
        mutation: glue.InsertData | glue.UpdateData | glue.DeleteData,
    ) -> dict[str, Any]:
        result = await self._operation_manager.perform_data_command_lakehouse(
            command=glue.DataCommand(
                mutations=[mutation],
                root_transaction_id=AmsdalAsyncTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalAsyncTransactionManager().transaction_id,
            ),
        )

        if not result.success:
            msg = f'Error while {mutation.__class__} class object schema in lakehouse: {result.message}'
            raise CommandError(msg) from result.exception

        # the first index 0 represents index of mutation, the second index - index of data
        return result.data[0][0].data  # type: ignore[index]

    async def fetch_historical_data(
        self,
        schema_reference: glue.SchemaReference,
        batch_size: int = MIGRATION_BATCH_SIZE,
        offset: int = 0,
    ) -> AsyncGenerator[dict[str, Any]]:
        is_deleted_field = glue.FieldReference(
            field=glue.Field(
                name=METADATA_FIELD,
                child=glue.Field(name='is_deleted'),
            ),
            table_name=schema_reference.name,
        )
        is_deleted_field.field.child.parent = is_deleted_field.field  # type: ignore[union-attr]
        query = glue.QueryStatement(
            table=schema_reference,
            where=glue.Conditions(
                glue.Condition(
                    field=is_deleted_field,
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=False),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
            limit=glue.LimitQuery(limit=batch_size, offset=offset),
            order_by=[
                glue.OrderByQuery(
                    field=glue.FieldReference(
                        field=glue.Field(name='updated_at'),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    direction=glue.OrderDirection.ASC,
                ),
            ],
        )

        result = await self._operation_manager.query_lakehouse(statement=query)

        if not result.success:
            msg = f'Error while fetching historical data: {result.message}'
            raise QueryError(msg) from result.exception

        for data in result.data or []:
            yield data.data

        if len(result.data or []) == batch_size:
            async for h_data in self.fetch_historical_data(schema_reference, batch_size, offset + batch_size):
                yield h_data

    async def search_latest_class_object(
        self,
        schema_reference: glue.SchemaReference,
        class_object_name: str,
    ) -> dict[str, Any] | None:
        _conditions = [
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=PRIMARY_PARTITION_KEY),
                    table_name=schema_reference.name,
                ),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(class_object_name),
            ),
            glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(value=True),
                ),
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=NEXT_VERSION_FIELD),
                        table_name=METADATA_TABLE_ALIAS,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=''),
                ),
                connector=glue.FilterConnector.OR,
            ),
        ]

        result = await self._operation_manager.query_lakehouse(
            statement=glue.QueryStatement(
                table=schema_reference,
                where=glue.Conditions(*_conditions),
                limit=glue.LimitQuery(limit=1),
            ),
        )

        if not result.success:
            msg = f'Error while searching latest class object version in lakehouse: {result.message}'
            raise QueryError(msg) from result.exception

        if result.data:
            return result.data[0].data
        return None
