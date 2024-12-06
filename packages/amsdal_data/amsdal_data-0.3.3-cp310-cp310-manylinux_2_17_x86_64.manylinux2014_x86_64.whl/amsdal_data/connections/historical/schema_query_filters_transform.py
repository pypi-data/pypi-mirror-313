from copy import copy

import amsdal_glue as glue
from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_utils.models.enums import Versions

from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_TABLE
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SCHEMA_NAME_FIELD
from amsdal_data.connections.constants import SCHEMA_VERSION_FIELD
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.command_builder import TABLE_NAME_VERSION_SEPARATOR
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager


class SchemaQueryFiltersTransform:
    def __init__(self, schema_query_filters: glue.Conditions | None) -> None:
        self.schema_query_filters = copy(schema_query_filters) if schema_query_filters else None
        self.schema_version_manager = HistoricalSchemaVersionManager()

    def transform(self) -> glue.Conditions | None:
        if not self.schema_query_filters:
            return self.schema_query_filters
        return self._transform(self.schema_query_filters)

    @staticmethod
    def process_data(data: list[glue.Schema]) -> list[glue.Schema]:
        result = []

        for item in data:
            _item = copy(item)

            if TABLE_NAME_VERSION_SEPARATOR in item.name:
                _name, _version = _item.name.split(TABLE_NAME_VERSION_SEPARATOR)
                _item.name = _name
                _item.version = _version

            for constraint in _item.constraints or []:
                if isinstance(constraint, glue.PrimaryKeyConstraint):
                    _item.name, _ = _item.name.rsplit('_x_', 1) if '_x_' in _item.name else (_item.name, None)

            result.append(_item)

        return result

    def _transform(self, item: glue.Conditions) -> glue.Conditions:
        _conditions: list[glue.Condition | glue.Conditions] = []
        _items = []

        for _condition in item.children:
            _condition = copy(_condition)

            if isinstance(_condition, glue.Conditions):
                _conditions.append(self._transform(_condition))
                continue

            if item.connector == glue.FilterConnector.OR:
                _conditions.append(self._transform_single_condition(_condition))
                continue

            if _condition.field.field.name not in (SCHEMA_NAME_FIELD, SCHEMA_VERSION_FIELD):
                _conditions.append(_condition)
                continue

            _items.append(_condition)

        _conditions.extend(self._transform_multiple_conditions(_items))

        return glue.Conditions(
            *_conditions,
            connector=item.connector,
            negated=item.negated,
        )

    @staticmethod
    def _transform_single_condition(condition: glue.Condition) -> glue.Conditions | glue.Condition:
        if condition.field.field.name == SCHEMA_NAME_FIELD:
            value = condition.value

            if value.value in (  # type: ignore[union-attr]
                TRANSACTION_TABLE,
                METADATA_TABLE,
                REFERENCE_TABLE,
                OBJECT_TABLE,
            ):
                value = copy(value)
                # value.value = value.value

            if condition.lookup == glue.FieldLookup.EQ:
                return glue.Conditions(
                    glue.Condition(
                        field=condition.field,
                        lookup=glue.FieldLookup.EQ,
                        negate=condition.negate,
                        value=value,
                    ),
                    glue.Condition(
                        field=condition.field,
                        lookup=glue.FieldLookup.STARTSWITH,
                        negate=condition.negate,
                        value=glue.Value(f'{value.value}{TABLE_NAME_VERSION_SEPARATOR}'),  # type: ignore[union-attr]
                    ),
                    connector=glue.FilterConnector.OR,
                )

            return glue.Condition(
                field=condition.field,
                lookup=condition.lookup,
                negate=condition.negate,
                value=value,
            )

        if condition.field.field.name == SCHEMA_VERSION_FIELD:
            if condition.lookup == glue.FieldLookup.EQ:
                return glue.Condition(
                    field=condition.field,
                    lookup=glue.FieldLookup.ENDSWITH,
                    negate=condition.negate,
                    value=glue.Value(f'{TABLE_NAME_VERSION_SEPARATOR}{condition.value.value}'),  # type: ignore[union-attr]
                )
            return condition
        return condition

    def _transform_multiple_conditions(self, items: list[glue.Condition]) -> list[glue.Condition]:
        if not items:
            return []

        if len(items) == 1:
            return [self._transform_single_condition(items[0])]  # type: ignore[list-item]

        if len(items) > 2:  # noqa: PLR2004
            msg = 'Only two conditions are supported'
            raise ValueError(msg)

        _name: glue.Condition = next(filter(lambda x: x.field.field.name == SCHEMA_NAME_FIELD, items))
        _version: glue.Condition = next(filter(lambda x: x.field.field.name == SCHEMA_VERSION_FIELD, items))
        _version_value = _version.value.value  # type: ignore[union-attr]

        if not _version_value:
            return [
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_NAME_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    negate=_name.negate,
                    value=glue.Value(_name.value.value),  # type: ignore[union-attr]
                ),
            ]

        if _version_value in (
            glue.Version.LATEST,
            Versions.LATEST,
            'LATEST',
        ):
            class_version = self.schema_version_manager.get_latest_schema_version(
                _name.value.value  # type: ignore[union-attr]
            )

            if not class_version:
                return [
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SCHEMA_NAME_FIELD),
                            table_name=SCHEMA_REGISTRY_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        negate=_name.negate,
                        value=glue.Value(_name.value.value),  # type: ignore[union-attr]
                    ),
                ]

            if class_version in (
                glue.Version.LATEST,
                Versions.LATEST,
                'LATEST',
            ):
                return [
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SCHEMA_NAME_FIELD),
                            table_name=SCHEMA_REGISTRY_TABLE,
                        ),
                        lookup=glue.FieldLookup.STARTSWITH,
                        negate=_name.negate,
                        value=glue.Value(f'{_name.value.value}{TABLE_NAME_VERSION_SEPARATOR}'),  # type: ignore[union-attr]
                    ),
                ]

            _version_value = class_version
        return [
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=SCHEMA_NAME_FIELD),
                    table_name=SCHEMA_REGISTRY_TABLE,
                ),
                lookup=glue.FieldLookup.EQ,
                negate=_name.negate,
                value=glue.Value(f'{_name.value.value}{TABLE_NAME_VERSION_SEPARATOR}{_version_value}'),  # type: ignore[union-attr]
            ),
        ]


class AsyncSchemaQueryFiltersTransform:
    def __init__(self, schema_query_filters: glue.Conditions | None) -> None:
        self.schema_query_filters = copy(schema_query_filters) if schema_query_filters else None
        self.schema_version_manager = AsyncHistoricalSchemaVersionManager()

    async def transform(self) -> glue.Conditions | None:
        if not self.schema_query_filters:
            return self.schema_query_filters
        return await self._transform(self.schema_query_filters)

    @staticmethod
    def process_data(data: list[glue.Schema]) -> list[glue.Schema]:
        result = []

        for item in data:
            _item = copy(item)

            if TABLE_NAME_VERSION_SEPARATOR in item.name:
                _name, _version = _item.name.split(TABLE_NAME_VERSION_SEPARATOR)
                _item.name = _name
                _item.version = _version

            for constraint in _item.constraints or []:
                if isinstance(constraint, glue.PrimaryKeyConstraint):
                    _item.name, _ = _item.name.rsplit('_x_', 1) if '_x_' in _item.name else (_item.name, None)

            result.append(_item)

        return result

    async def _transform(self, item: glue.Conditions) -> glue.Conditions:
        _conditions: list[glue.Condition | glue.Conditions] = []
        _items = []

        for _condition in item.children:
            _condition = copy(_condition)

            if isinstance(_condition, glue.Conditions):
                _conditions.append(await self._transform(_condition))
                continue

            if item.connector == glue.FilterConnector.OR:
                _conditions.append(self._transform_single_condition(_condition))
                continue

            if _condition.field.field.name not in (SCHEMA_NAME_FIELD, SCHEMA_VERSION_FIELD):
                _conditions.append(_condition)
                continue

            _items.append(_condition)

        _conditions.extend(await self._transform_multiple_conditions(_items))

        return glue.Conditions(
            *_conditions,
            connector=item.connector,
            negated=item.negated,
        )

    @staticmethod
    def _transform_single_condition(condition: glue.Condition) -> glue.Conditions | glue.Condition:
        if condition.field.field.name == SCHEMA_NAME_FIELD:
            value = condition.value

            if value.value in (  # type: ignore[union-attr]
                TRANSACTION_TABLE,
                METADATA_TABLE,
                REFERENCE_TABLE,
                OBJECT_TABLE,
            ):
                value = copy(value)
                # value.value = value.value

            if condition.lookup == glue.FieldLookup.EQ:
                return glue.Conditions(
                    glue.Condition(
                        field=condition.field,
                        lookup=glue.FieldLookup.EQ,
                        negate=condition.negate,
                        value=value,
                    ),
                    glue.Condition(
                        field=condition.field,
                        lookup=glue.FieldLookup.STARTSWITH,
                        negate=condition.negate,
                        value=glue.Value(f'{value.value}{TABLE_NAME_VERSION_SEPARATOR}'),  # type: ignore[union-attr]
                    ),
                    connector=glue.FilterConnector.OR,
                )

            return glue.Condition(
                field=condition.field,
                lookup=condition.lookup,
                negate=condition.negate,
                value=value,
            )

        if condition.field.field.name == SCHEMA_VERSION_FIELD:
            if condition.lookup == glue.FieldLookup.EQ:
                return glue.Condition(
                    field=condition.field,
                    lookup=glue.FieldLookup.ENDSWITH,
                    negate=condition.negate,
                    value=glue.Value(f'{TABLE_NAME_VERSION_SEPARATOR}{condition.value.value}'),  # type: ignore[union-attr]
                )
            return condition
        return condition

    async def _transform_multiple_conditions(self, items: list[glue.Condition]) -> list[glue.Condition]:
        if not items:
            return []

        if len(items) == 1:
            return [self._transform_single_condition(items[0])]  # type: ignore[list-item]

        if len(items) > 2:  # noqa: PLR2004
            msg = 'Only two conditions are supported'
            raise ValueError(msg)

        _name: glue.Condition = next(filter(lambda x: x.field.field.name == SCHEMA_NAME_FIELD, items))
        _version: glue.Condition = next(filter(lambda x: x.field.field.name == SCHEMA_VERSION_FIELD, items))
        _version_value = _version.value.value  # type: ignore[union-attr]

        if not _version_value:
            return [
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=SCHEMA_NAME_FIELD),
                        table_name=SCHEMA_REGISTRY_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    negate=_name.negate,
                    value=glue.Value(_name.value.value),  # type: ignore[union-attr]
                ),
            ]

        if _version_value in (
            glue.Version.LATEST,
            Versions.LATEST,
            'LATEST',
        ):
            class_version = await self.schema_version_manager.get_latest_schema_version(
                _name.value.value  # type: ignore[union-attr]
            )

            if not class_version:
                return [
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SCHEMA_NAME_FIELD),
                            table_name=SCHEMA_REGISTRY_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        negate=_name.negate,
                        value=glue.Value(_name.value.value),  # type: ignore[union-attr]
                    ),
                ]

            if class_version in (
                glue.Version.LATEST,
                Versions.LATEST,
                'LATEST',
            ):
                return [
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SCHEMA_NAME_FIELD),
                            table_name=SCHEMA_REGISTRY_TABLE,
                        ),
                        lookup=glue.FieldLookup.STARTSWITH,
                        negate=_name.negate,
                        value=glue.Value(f'{_name.value.value}{TABLE_NAME_VERSION_SEPARATOR}'),  # type: ignore[union-attr]
                    ),
                ]

            _version_value = class_version
        return [
            glue.Condition(
                field=glue.FieldReference(
                    field=glue.Field(name=SCHEMA_NAME_FIELD),
                    table_name=SCHEMA_REGISTRY_TABLE,
                ),
                lookup=glue.FieldLookup.EQ,
                negate=_name.negate,
                value=glue.Value(f'{_name.value.value}{TABLE_NAME_VERSION_SEPARATOR}{_version_value}'),  # type: ignore[union-attr]
            ),
        ]
