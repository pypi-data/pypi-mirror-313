import amsdal_glue as glue
from amsdal_data.connections.constants import METADATA_TABLE as METADATA_TABLE, OBJECT_TABLE as OBJECT_TABLE, REFERENCE_TABLE as REFERENCE_TABLE, TRANSACTION_TABLE as TRANSACTION_TABLE
from amsdal_data.connections.historical.schema_version_manager import AsyncHistoricalSchemaVersionManager as AsyncHistoricalSchemaVersionManager, HistoricalSchemaVersionManager as HistoricalSchemaVersionManager
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import NestedFieldTransform as NestedFieldTransform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import OperatorConstructor as OperatorConstructor
from amsdal_glue_core.common.operations.mutations.data import DataMutation as DataMutation
from collections.abc import Callable as Callable
from typing import Any

TABLE_NAME_VERSION_SEPARATOR: str

def build_historical_sql_data_command(mutation: DataMutation, value_placeholder: str = '?', table_separator: str = '.', operator_constructor: OperatorConstructor = ..., table_quote: str = '', field_quote: str = '', value_transform: Callable[[Any], Any] = ..., nested_field_transform: NestedFieldTransform = ...) -> tuple[str, list[Any]]:
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
def _build_historical_sql_insert_data(command: glue.InsertData, value_placeholder: str, table_separator: str = '.', table_quote: str = '', field_quote: str = '', value_transform: Callable[[Any], Any] = ...) -> tuple[str, list[Any]]: ...
def _build_historical_sql_update_data(command: glue.UpdateData, value_placeholder: str, table_separator: str, operator_constructor: OperatorConstructor = ..., table_quote: str = '', field_quote: str = '', value_transform: Callable[[Any], Any] = ..., nested_field_transform: NestedFieldTransform = ...) -> tuple[str, list[Any]]: ...
def _build_historical_sql_delete_data(command: glue.DeleteData, value_placeholder: str, table_separator: str, operator_constructor: OperatorConstructor = ..., table_quote: str = '', field_quote: str = '', value_transform: Callable[[Any], Any] = ..., nested_field_transform: NestedFieldTransform = ...) -> tuple[str, list[Any]]: ...
def build_historical_table_name(schema_reference: glue.SchemaReference) -> str: ...
async def async_build_historical_table_name(schema_reference: glue.SchemaReference) -> str: ...
def format_historical_table_name(name: str, version: str) -> str: ...
def _adjust_field_table_name(field_reference: glue.FieldReference, schema_reference: glue.SchemaReference) -> glue.FieldReference: ...
def _adjust_conditions_table_name(conditions: glue.Conditions, schema_reference: glue.SchemaReference) -> glue.Conditions: ...
