import amsdal_glue as glue
from _typeshed import Incomplete
from amsdal_data.connections.constants import METADATA_TABLE as METADATA_TABLE, PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, REFERENCE_TABLE as REFERENCE_TABLE, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY, TRANSACTION_TABLE as TRANSACTION_TABLE

OBJECT_ID_FIELD: str
OBJECT_VERSION_FIELD: str
METADATA_FIELD: str
NEXT_VERSION_FIELD: str
MODEL_TABLE_ALIAS: str
METADATA_TABLE_ALIAS: str
METADATA_SELECT_EXPRESSION: Incomplete
PG_METADATA_SELECT_EXPRESSION: Incomplete

class DataQueryTransform:
    query: Incomplete
    def __init__(self, query: glue.QueryStatement) -> None: ...
    def transform(self, metadata_select_expression: str = ...) -> glue.QueryStatement: ...
    def _transform_query(self, query: glue.QueryStatement, metadata_select_expression: str = ...) -> glue.QueryStatement: ...
    def _transform_conditions(self, conditions: glue.Conditions | None) -> glue.Conditions | None: ...
    @staticmethod
    def _transform_metadata_fields_in_only(only: list[glue.FieldReference | glue.FieldReferenceAliased] | None) -> list[glue.FieldReference] | None: ...
    @staticmethod
    def _transform_metadata_fields_in_order_by(order_by: list[glue.OrderByQuery] | None) -> list[glue.OrderByQuery] | None: ...
    def _enrich_with_metadata_join(self, query: glue.QueryStatement, metadata_select_expression: str = ...) -> glue.QueryStatement: ...
