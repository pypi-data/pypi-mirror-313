from copy import copy

import amsdal_glue as glue

from amsdal_data.connections.historical.command_builder import async_build_historical_table_name
from amsdal_data.connections.historical.command_builder import build_historical_table_name


class _TableNameTransform:
    def __init__(self, query: glue.QueryStatement) -> None:
        self.query = copy(query)

    @property
    def table_name(self) -> str:
        return self._resolve_table_name(self.query)

    def _resolve_table_name(self, query: glue.QueryStatement) -> str:
        if isinstance(query.table, glue.SubQueryStatement):
            return self._resolve_table_name(query.table.query)
        return query.table.name


class TableNameTransform(_TableNameTransform):
    def transform(self) -> glue.QueryStatement:
        return self._process_table_names(self.query)

    @classmethod
    def _process_table_names(cls, query: glue.QueryStatement) -> glue.QueryStatement:
        _query = copy(query)
        cls.process_table_name(_query.table)

        if _query.annotations:
            for _annotation in _query.annotations:
                if isinstance(_annotation.value, glue.SubQueryStatement):
                    cls._process_table_names(_annotation.value.query)

        if _query.joins:
            for _join in _query.joins:
                cls.process_table_name(_join.table)

        return _query

    @classmethod
    def process_table_name(cls, table: glue.SchemaReference | glue.SubQueryStatement) -> None:
        if isinstance(table, glue.SchemaReference):
            _original_name = table.name
            table.name = build_historical_table_name(table)
            table.alias = table.alias or _original_name
        else:
            cls._process_table_names(table.query)


class AsyncTableNameTransform(_TableNameTransform):

    async def transform(self) -> glue.QueryStatement:
        return await self._process_table_names(self.query)

    @classmethod
    async def _process_table_names(cls, query: glue.QueryStatement) -> glue.QueryStatement:
        _query = copy(query)
        await cls.process_table_name(_query.table)

        if _query.annotations:
            for _annotation in _query.annotations:
                if isinstance(_annotation.value, glue.SubQueryStatement):
                    await cls._process_table_names(_annotation.value.query)

        if _query.joins:
            for _join in _query.joins:
                await cls.process_table_name(_join.table)

        return _query

    @classmethod
    async def process_table_name(cls, table: glue.SchemaReference | glue.SubQueryStatement) -> None:
        if isinstance(table, glue.SchemaReference):
            _original_name = table.name
            table.name = await async_build_historical_table_name(table)
            table.alias = table.alias or _original_name
        else:
            await cls._process_table_names(table.query)
