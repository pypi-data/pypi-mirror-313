from collections.abc import Callable
from typing import Any

import amsdal_glue as glue
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import NestedFieldTransform
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import OperatorConstructor
from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.enums import Versions

from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_TABLE
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager

TABLE_NAME_VERSION_SEPARATOR = '__v__'


def build_historical_sql_data_command(
    mutation: DataMutation,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    """
    Builds an SQL command for the given data mutation.

    Args:
        mutation (DataMutation): The data mutation to be converted to an SQL command.
        value_placeholder (str, optional): The placeholder for values in the SQL command. Defaults to '?'.
        table_separator (str, optional): The separator for table names. Defaults to '.'.
        operator_constructor (Callable, optional): The function to construct operators.
                                                   Defaults to default_operator_constructor.
        table_quote (str, optional): The quote character for table names. Defaults to ''.
        field_quote (str, optional): The quote character for field names. Defaults to ''.
        value_transform (Callable, optional): The function to transform values. Defaults to lambda x: x.
        nested_field_transform (Callable, optional): The function to transform nested fields.
                                                     Defaults to default_nested_field_transform.

    Returns:
        tuple[str, list[Any]]: The SQL command and the list of values.
    """
    if isinstance(mutation, glue.InsertData):
        return _build_historical_sql_insert_data(
            mutation,
            value_placeholder,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
        )

    if isinstance(mutation, glue.UpdateData):
        return _build_historical_sql_update_data(
            mutation,
            value_placeholder,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

    if isinstance(mutation, glue.DeleteData):
        return _build_historical_sql_delete_data(
            mutation,
            value_placeholder,
            table_separator,
            operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

    msg = f'Unsupported command type: {type(mutation)}'
    raise NotImplementedError(msg)


def _build_historical_sql_insert_data(
    command: glue.InsertData,
    value_placeholder: str,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
) -> tuple[str, list[Any]]:
    _namespace_prefix = (
        f'{table_quote}{command.schema.namespace}{table_quote}{table_separator}' if command.schema.namespace else ''
    )
    _table_name = build_historical_table_name(command.schema)
    stmt = f'INSERT INTO {_namespace_prefix}{table_quote}{_table_name}{table_quote}'

    if not command.data:
        msg = 'No data provided for insert operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted({key for data in command.data for key in data.data})
    placeholders = [[value_placeholder] * len(keys)] * len(command.data)

    if command.data:
        stmt += ' ('
        stmt += ', '.join(f'{field_quote}{key}{field_quote}' for key in keys)
        stmt += ') VALUES '
        stmt += ', '.join(f'({", ".join(row)})' for row in placeholders)
        values.extend(value_transform(data.data.get(key)) for data in command.data for key in keys)

    return stmt, values


def _build_historical_sql_update_data(
    command: glue.UpdateData,
    value_placeholder: str,
    table_separator: str,
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    _namespace_prefix = (
        f'{table_quote}{command.schema.namespace}{table_quote}{table_separator}' if command.schema.namespace else ''
    )
    _table_name = build_historical_table_name(command.schema)
    stmt = f'UPDATE {_namespace_prefix}{table_quote}{_table_name}{table_quote}'

    if command.schema.alias:
        stmt += f' AS {table_quote}{command.schema.alias}{table_quote}'

    if not command.data:
        msg = 'No data provided for update operation'
        raise ValueError(msg)

    values: list[Any] = []

    keys = sorted(set(command.data.data))

    if command.data:
        stmt += ' SET '
        stmt += ', '.join(f'{field_quote}{key}{field_quote} = {value_placeholder}' for key in keys)
        values.extend(value_transform(command.data.data.get(key)) for key in keys)

    if command.query:
        _query = _adjust_conditions_table_name(command.query, command.schema)
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)

    return stmt, values


def _build_historical_sql_delete_data(
    command: glue.DeleteData,
    value_placeholder: str,
    table_separator: str,
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    _namespace_prefix = (
        f'{table_quote}{command.schema.namespace}{table_quote}{table_separator}' if command.schema.namespace else ''
    )
    stmt = f'DELETE FROM {_namespace_prefix}{table_quote}{command.schema.name}{table_quote}'  # noqa: S608

    if command.schema.alias:
        stmt += f' AS {table_quote}{command.schema.alias}{table_quote}'

    values = []

    if command.query:
        where, where_values = build_conditions(
            conditions=command.query,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )

        stmt += f' WHERE {where}'
        values.extend(where_values)
    return stmt, values


def build_historical_table_name(
    schema_reference: glue.SchemaReference,
) -> str:
    if schema_reference.name in (
        TRANSACTION_TABLE,
        METADATA_TABLE,
        REFERENCE_TABLE,
        OBJECT_TABLE,
    ):
        return schema_reference.name

    class_version_manager = HistoricalSchemaVersionManager()
    _version = schema_reference.version

    if _version in (glue.Version.LATEST, Versions.LATEST):
        _version = class_version_manager.get_latest_schema_version(schema_reference.name)

    if _version in (glue.Version.LATEST, Versions.LATEST) or not _version:
        # Still latest version means that there is no historical table
        return schema_reference.name

    return format_historical_table_name(schema_reference.name, _version)


async def async_build_historical_table_name(
    schema_reference: glue.SchemaReference,
) -> str:
    if schema_reference.name in (
        TRANSACTION_TABLE,
        METADATA_TABLE,
        REFERENCE_TABLE,
        OBJECT_TABLE,
    ):
        return schema_reference.name

    class_version_manager = AsyncHistoricalSchemaVersionManager()
    _version = schema_reference.version

    if _version in (glue.Version.LATEST, Versions.LATEST):
        _version = await class_version_manager.get_latest_schema_version(schema_reference.name)

    if _version in (glue.Version.LATEST, Versions.LATEST) or not _version:
        # Still latest version means that there is no historical table
        return schema_reference.name

    return format_historical_table_name(schema_reference.name, _version)


def format_historical_table_name(
    name: str,
    version: str,
) -> str:
    if not version:
        return name

    return f'{name}{TABLE_NAME_VERSION_SEPARATOR}{version}'


def _adjust_field_table_name(
    field_reference: glue.FieldReference,
    schema_reference: glue.SchemaReference,
) -> glue.FieldReference:
    if field_reference.table_name == schema_reference.name and not schema_reference.alias:
        return glue.FieldReference(
            field=field_reference.field,
            table_name=build_historical_table_name(schema_reference),
        )
    return field_reference


def _adjust_conditions_table_name(
    conditions: glue.Conditions,
    schema_reference: glue.SchemaReference,
) -> glue.Conditions:
    result = glue.Conditions(
        connector=conditions.connector,
        negated=conditions.negated,
    )
    for child in conditions.children:
        if isinstance(child, glue.Condition):
            _child = glue.Condition(
                field=_adjust_field_table_name(child.field, schema_reference),
                lookup=child.lookup,
                value=child.value,
            )

            if isinstance(_child.value, glue.FieldReference):
                _child.value = _adjust_field_table_name(_child.value, schema_reference)

            result.children.append(_child)
        elif isinstance(child, glue.Conditions):
            result.children.append(_adjust_conditions_table_name(child, schema_reference))
    return result
