from copy import copy

import amsdal_glue as glue
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.enums import Versions

from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_TABLE
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.data_mutation_transform import DataMutationTransform
from amsdal_data.connections.historical.data_query_transform import DataQueryTransform
from amsdal_data.connections.historical.query_builder import pull_out_filter_from_query
from amsdal_data.connections.historical.query_builder import sort_items
from amsdal_data.connections.historical.query_builder import split_conditions
from amsdal_data.connections.historical.schema_command_transform import SchemaCommandExecutor
from amsdal_data.connections.historical.schema_query_filters_transform import SchemaQueryFiltersTransform
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.connections.historical.table_name_transform import TableNameTransform


class SqliteHistoricalConnection(glue.SqliteConnection):
    def __init__(self) -> None:
        super().__init__()
        self.schema_version_manager = HistoricalSchemaVersionManager()

    def query(self, query: glue.QueryStatement) -> list[glue.Data]:
        _transform = DataQueryTransform(query)
        _query = self._process_group_by(_transform.transform())

        _table_transform = TableNameTransform(_query)

        if _table_transform.table_name in (METADATA_TABLE, REFERENCE_TABLE, TRANSACTION_TABLE):
            return super().query(_table_transform.transform())

        items: list[glue.Data] = []
        queries = self._build_queries_by_version(_query)

        for _query_version in queries:
            # Historical table name
            _table_transform = TableNameTransform(_query_version)
            items.extend(super().query(_table_transform.transform()))

        if len(queries) > 1:
            items = sort_items(items, _query.order_by)
            items = self._apply_pagination(items, _query.limit)

        return items

    def _process_group_by(self, query: glue.QueryStatement) -> glue.QueryStatement:
        if ((query.only and not query.aggregations) or query.order_by) and query.table.name not in (  # type: ignore[union-attr]
            METADATA_TABLE,
            REFERENCE_TABLE,
            TRANSACTION_TABLE,
        ):
            group_by = []

            if query.only and not query.aggregations:
                for _field in query.only:
                    if isinstance(_field, glue.FieldReferenceAliased):
                        _field_reference = glue.FieldReference(
                            field=_field.field,
                            table_name=_field.table_name,
                            namespace=_field.namespace,
                        )
                    else:
                        _field_reference = _field

                    group_by.append(glue.GroupByQuery(field=_field_reference))

            if len(group_by) == 1 and group_by[0].field.field.name == '*':
                group_by = [
                    glue.GroupByQuery(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=query.table.alias or query.table.name,  # type: ignore[union-attr]
                        ),
                    ),
                    glue.GroupByQuery(
                        field=glue.FieldReference(
                            field=glue.Field(name=SECONDARY_PARTITION_KEY),
                            table_name=query.table.alias or query.table.name,  # type: ignore[union-attr]
                        ),
                    ),
                ]

            if query.order_by:
                for order_field in query.order_by:
                    group_by.append(glue.GroupByQuery(field=order_field.field))

            query.group_by = group_by

        if query.joins:
            for _join in query.joins:
                _table = _join.table

                if isinstance(_table, glue.SubQueryStatement):
                    _table.query = self._process_group_by(_table.query)

        return query

    def query_schema(self, filters: glue.Conditions | None = None) -> list[glue.Schema]:
        _transform = SchemaQueryFiltersTransform(filters)
        _conditions = _transform.transform()

        data = super().query_schema(_conditions)

        return _transform.process_data(data)

    def _run_mutation(self, mutation: DataMutation) -> list[glue.Data] | None:
        _transform = DataMutationTransform(self, mutation)
        _mutations = _transform.transform()
        _result: list[glue.Data] = []

        for _mutation in _mutations:
            super()._run_mutation(_mutation)

        return _transform.data

    def run_schema_command(self, command: glue.SchemaCommand) -> list[glue.Schema | None]:
        _executor = SchemaCommandExecutor(self, command)

        return _executor.execute()

    def run_schema_mutation(self, mutation: glue.SchemaMutation) -> glue.Schema | None:
        return super()._run_schema_mutation(mutation)

    def _build_queries_by_version(self, query: glue.QueryStatement) -> list[glue.QueryStatement]:
        if not query.where:
            return self._to_queries_by_version(query.table.version, query)  # type: ignore[arg-type, union-attr]

        queries_by_version: dict[str, glue.QueryStatement] = {}
        field = glue.Field(name='_address', child=glue.Field(name='class_version'))
        field.child.parent = field  # type: ignore[union-attr]

        for _conditions in split_conditions(query.where):
            _class_versions, _query = pull_out_filter_from_query(_conditions, field)

            if not _class_versions:
                _class_versions = {query.table.version}  # type: ignore[union-attr]

            if _query is None:
                _query = ~glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=PRIMARY_PARTITION_KEY),
                            table_name=query.table.name,  # type: ignore[union-attr]
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value('_empty-'),
                    ),
                )

            for _class_version in _class_versions:
                if _class_version in (glue.Version.ALL, Versions.ALL):
                    _versions = set()
                    for _item_version in self.schema_version_manager.get_all_schema_versions(query.table.name):  # type: ignore[union-attr]
                        if _item_version or query.table.name in {  # type: ignore[union-attr]
                            TRANSACTION_TABLE,
                            METADATA_TABLE,
                            REFERENCE_TABLE,
                            OBJECT_TABLE,
                        }:
                            _versions.add(_item_version)
                elif _class_version in (glue.Version.LATEST, Versions.LATEST):
                    _versions = {self.schema_version_manager.get_latest_schema_version(query.table.name)}  # type: ignore[union-attr]
                else:
                    _versions = {_class_version}

                for _specific_current_version in _versions:
                    _query_version = copy(query)
                    _query_version.table = copy(query.table)
                    _query_version.table.version = _specific_current_version  # type: ignore[union-attr]
                    _query_version.where = _query

                    if _specific_current_version not in queries_by_version:
                        queries_by_version[_specific_current_version] = _query_version
                    else:
                        _q_version = queries_by_version[_specific_current_version]

                        if _q_version.where is not None:
                            _q_version.where |= _query

        return list(queries_by_version.values())

    def _to_queries_by_version(
        self,
        version: glue.Version | Versions,
        query: glue.QueryStatement,
    ) -> list[glue.QueryStatement]:
        queries = []

        _table = query.table

        if isinstance(_table, glue.SubQueryStatement):
            return [query]

        if version in (glue.Version.ALL, Versions.ALL):
            for _class_version in self.schema_version_manager.get_all_schema_versions(_table.name):
                _query = copy(query)
                _query.table = copy(_table)
                _query.table.version = _class_version
                queries.append(_query)
        elif version in (glue.Version.LATEST, Versions.LATEST):
            _latest_class_version = self.schema_version_manager.get_latest_schema_version(_table.name)
            _table.version = _latest_class_version
            queries.append(query)
        else:
            queries.append(query)

        return queries

    @staticmethod
    def _apply_pagination(items: list[glue.Data], limit: glue.LimitQuery | None) -> list[glue.Data]:
        if limit is None or not limit.limit:
            return items

        return items[slice(limit.offset, limit.offset + limit.limit)]

    def _transform_schema_to_historical(self, schema: glue.Schema) -> None:
        if schema.name in (
            TRANSACTION_TABLE,
            METADATA_TABLE,
            REFERENCE_TABLE,
        ):
            return

        if next((True for _property in schema.properties if _property.name == SECONDARY_PARTITION_KEY), False):
            return

        schema.properties.append(
            glue.PropertySchema(
                name=SECONDARY_PARTITION_KEY,
                type=str,
                required=True,
            ),
        )

        pk = glue.PrimaryKeyConstraint(
            name=f'pk_{schema.name.lower()}',
            fields=[PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY],
        )
        schema.constraints = [
            _constraint
            for _constraint in (schema.constraints or [])
            if not isinstance(_constraint, glue.PrimaryKeyConstraint)
        ]
        schema.constraints.append(pk)
