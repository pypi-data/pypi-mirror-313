from copy import copy
from copy import deepcopy

import amsdal_glue as glue

from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.constants import TRANSACTION_TABLE

OBJECT_ID_FIELD = 'object_id'
OBJECT_VERSION_FIELD = 'object_version'
METADATA_FIELD = '_metadata'
NEXT_VERSION_FIELD = 'next_version'

MODEL_TABLE_ALIAS = 't1'
METADATA_TABLE_ALIAS = 't2'

METADATA_SELECT_EXPRESSION = f"""
json_object(
    '_next_version', {METADATA_TABLE_ALIAS}.next_version,
    'object_id', {METADATA_TABLE_ALIAS}.object_id,
    'object_version', {METADATA_TABLE_ALIAS}.object_version,
    'prior_version', {METADATA_TABLE_ALIAS}.prior_version,
    'class_schema_reference', json({METADATA_TABLE_ALIAS}.class_schema_reference),
    'class_meta_schema_reference', json({METADATA_TABLE_ALIAS}.class_meta_schema_reference),
    'is_deleted', {METADATA_TABLE_ALIAS}.is_deleted,
    'created_at', {METADATA_TABLE_ALIAS}.created_at,
    'updated_at', {METADATA_TABLE_ALIAS}.updated_at,
    'transaction', json({METADATA_TABLE_ALIAS}.'transaction')
)
"""
PG_METADATA_SELECT_EXPRESSION = f"""
json_build_object(
    '_next_version', json_agg({METADATA_TABLE_ALIAS}."next_version")->0,
    'object_id', json_agg({METADATA_TABLE_ALIAS}.object_id)->0,
    'object_version', json_agg({METADATA_TABLE_ALIAS}.object_version)->0,
    'prior_version', json_agg({METADATA_TABLE_ALIAS}.prior_version)->0,
    'class_schema_reference', json_agg(to_json({METADATA_TABLE_ALIAS}.class_schema_reference))->0,
    'class_meta_schema_reference', json_agg(to_json({METADATA_TABLE_ALIAS}.class_meta_schema_reference))->0,
    'is_deleted', json_agg({METADATA_TABLE_ALIAS}.is_deleted)->0,
    'created_at', json_agg({METADATA_TABLE_ALIAS}.created_at)->0,
    'updated_at', json_agg({METADATA_TABLE_ALIAS}.updated_at)->0,
    'transaction', json_agg(to_json({METADATA_TABLE_ALIAS}."transaction"))->0
)
"""


class DataQueryTransform:
    def __init__(self, query: glue.QueryStatement):
        self.query = deepcopy(query)

    def transform(self, metadata_select_expression: str = METADATA_SELECT_EXPRESSION) -> glue.QueryStatement:
        return self._transform_query(self.query, metadata_select_expression)

    def _transform_query(
        self,
        query: glue.QueryStatement,
        metadata_select_expression: str = METADATA_SELECT_EXPRESSION,
    ) -> glue.QueryStatement:
        if isinstance(query.table, glue.SubQueryStatement):
            query.table.query = self._transform_query(
                query.table.query,
                metadata_select_expression=metadata_select_expression,
            )
        else:
            query = self._enrich_with_metadata_join(query, metadata_select_expression=metadata_select_expression)
            query.where = self._transform_conditions(query.where)
            query.only = self._transform_metadata_fields_in_only(query.only)
            query.order_by = self._transform_metadata_fields_in_order_by(query.order_by)

        for annotation in query.annotations or []:
            if isinstance(annotation.value, glue.SubQueryStatement):
                annotation.value.query = self._transform_query(
                    annotation.value.query,
                    metadata_select_expression=metadata_select_expression,
                )

        for join in query.joins or []:
            if isinstance(join.table, glue.SubQueryStatement) and join.table.alias != METADATA_TABLE_ALIAS:
                join.table.query = self._transform_query(
                    join.table.query,
                    metadata_select_expression=metadata_select_expression,
                )
            elif condition := self._transform_conditions(join.on):
                join.on = condition

        return query

    def _transform_conditions(self, conditions: glue.Conditions | None) -> glue.Conditions | None:
        if not conditions:
            return None

        for _index, _condition in enumerate(conditions.children):
            if isinstance(_condition, glue.Conditions):
                if condition := self._transform_conditions(_condition):
                    conditions.children[_index] = condition
                continue

            # transform fields
            if _condition.field.field.name == METADATA_FIELD and _condition.field.field.child:
                _condition.field = glue.FieldReference(
                    field=_condition.field.field.child,
                    table_name=METADATA_TABLE_ALIAS,
                )

        return conditions

    @staticmethod
    def _transform_metadata_fields_in_only(
        only: list[glue.FieldReference | glue.FieldReferenceAliased] | None,
    ) -> list[glue.FieldReference] | None:
        if not only:
            return None

        for _index, _field in enumerate(only):
            if _field.field.name == METADATA_FIELD and _field.field.child:
                only[_index] = glue.FieldReference(
                    field=_field.field.child,
                    table_name=METADATA_TABLE_ALIAS,
                )

        return only

    @staticmethod
    def _transform_metadata_fields_in_order_by(
        order_by: list[glue.OrderByQuery] | None,
    ) -> list[glue.OrderByQuery] | None:
        if not order_by:
            return None

        for _index, _order_by in enumerate(order_by):
            if _order_by.field.field.name == METADATA_FIELD and _order_by.field.field.child:
                order_by[_index].field = glue.FieldReference(
                    field=_order_by.field.field.child,
                    table_name=METADATA_TABLE_ALIAS,
                )

        return order_by

    def _enrich_with_metadata_join(
        self,
        query: glue.QueryStatement,
        metadata_select_expression: str = METADATA_SELECT_EXPRESSION,
    ) -> glue.QueryStatement:
        _query = copy(query)

        if isinstance(_query.table, glue.SubQueryStatement):
            return self._enrich_with_metadata_join(
                _query.table.query,
                metadata_select_expression=metadata_select_expression,
            )

        if _query.table.name in (
            TRANSACTION_TABLE,
            METADATA_TABLE,
            REFERENCE_TABLE,
        ):
            return _query

        # check if metadata is joined already
        _joins = _query.joins or []

        for join in _joins:
            if isinstance(join.table, glue.SchemaReference):
                _table_name = join.table.alias or join.table.name
            else:
                _table_name = join.table.alias

            if _table_name == METADATA_TABLE_ALIAS:
                return _query

        if not _query.only and not _query.aggregations:
            _query.only = [
                glue.FieldReference(
                    field=glue.Field(name='*'),
                    table_name=_query.table.alias or _query.table.name,
                ),
            ]

        _query.annotations = _query.annotations or []

        _query.annotations.append(
            glue.AnnotationQuery(
                value=glue.ExpressionAnnotation(
                    expression=glue.RawExpression(metadata_select_expression),
                    alias=METADATA_FIELD,
                ),
            ),
        )

        # metadata table does not exist in joins, let's add
        _joins.append(
            glue.JoinQuery(
                table=glue.SubQueryStatement(
                    query=glue.QueryStatement(
                        table=glue.SchemaReference(
                            name=METADATA_TABLE,
                            alias='_m',
                            version=glue.Version.LATEST,
                        ),
                        only=[
                            glue.FieldReference(
                                field=glue.Field(name='*'),
                                table_name='_m',
                            ),
                        ],
                        annotations=[
                            glue.AnnotationQuery(
                                value=glue.SubQueryStatement(
                                    query=glue.QueryStatement(
                                        only=[
                                            glue.FieldReference(
                                                field=glue.Field(name='object_version'),
                                                table_name='_m2',
                                            ),
                                        ],
                                        table=glue.SchemaReference(
                                            name=METADATA_TABLE,
                                            version=glue.Version.LATEST,
                                            alias='_m2',
                                        ),
                                        where=glue.Conditions(
                                            glue.Condition(
                                                field=glue.FieldReference(
                                                    field=glue.Field(name='object_version'),
                                                    table_name='_m',
                                                ),
                                                lookup=glue.FieldLookup.EQ,
                                                value=glue.FieldReference(
                                                    field=glue.Field(name='prior_version'),
                                                    table_name='_m2',
                                                ),
                                            ),
                                            glue.Condition(
                                                field=glue.FieldReference(
                                                    field=glue.Field(name='object_id'),
                                                    table_name='_m',
                                                ),
                                                lookup=glue.FieldLookup.EQ,
                                                value=glue.FieldReference(
                                                    field=glue.Field(name='object_id'),
                                                    table_name='_m2',
                                                ),
                                            ),
                                            connector=glue.FilterConnector.AND,
                                        ),
                                    ),
                                    alias=NEXT_VERSION_FIELD,
                                ),
                            ),
                        ],
                    ),
                    alias=METADATA_TABLE_ALIAS,
                ),
                join_type=glue.JoinType.INNER,
                on=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=_query.table.alias or _query.table.name,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.FieldReference(
                            field=glue.Field(name='object_id'),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=SECONDARY_PARTITION_KEY),
                            table_name=_query.table.alias or _query.table.name,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.FieldReference(
                            field=glue.Field(name='object_version'),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                    ),
                    connector=glue.FilterConnector.AND,
                ),
            ),
        )

        _query.joins = _joins

        return _query
