from datetime import date
from datetime import datetime
from typing import Any

import amsdal_glue as glue
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_utils.config.data_models.repository_config import RepositoryConfig
from amsdal_utils.models.data_models.enums import CoreTypes
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.utils.classes import import_class
from amsdal_utils.utils.singleton import Singleton

from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.db_alias_map import CONNECTION_BACKEND_ALIASES


class SchemaManagerBase:
    pass


class SchemaManagerHandler(metaclass=Singleton):
    def __init__(self) -> None:
        self._schema_manager: SchemaManagerBase | None = None

    def set_schema_manager(self, schema_manager: SchemaManagerBase) -> None:
        self._schema_manager = schema_manager

    def get_schema_manager(self) -> SchemaManagerBase:
        if self._schema_manager is None:
            msg = 'Schema manager is not set.'
            raise ValueError(msg)
        return self._schema_manager


def resolve_backend_class(backend: str) -> type[ConnectionBase]:
    if backend in CONNECTION_BACKEND_ALIASES:
        backend = CONNECTION_BACKEND_ALIASES[backend]

    return import_class(backend)


def get_schemas_for_connection_name(connection_name: str, repository_config: RepositoryConfig) -> list[str | None]:
    if connection_name == repository_config.default:
        return [None]

    return [
        _schema_name
        for _schema_name, _connection_name in repository_config.models.items()
        if _connection_name == connection_name
    ]


def object_schema_to_glue_schema(
    object_schema: ObjectSchema,
    *,
    is_lakehouse_only: bool = False,
) -> glue.Schema:
    from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY

    _pk_constraint = glue.PrimaryKeyConstraint(
        name=f'pk_{object_schema.title.lower()}',
        fields=[PRIMARY_PARTITION_KEY],
    )
    _schema = glue.Schema(
        name=object_schema.title,
        version=glue.Version.LATEST,
        properties=[
            glue.PropertySchema(
                name=PRIMARY_PARTITION_KEY,
                type=str,
                required=True,
            ),
        ],
        constraints=[
            _pk_constraint,
        ],
        indexes=[],
    )

    if is_lakehouse_only:
        _schema.properties.append(
            glue.PropertySchema(
                name=SECONDARY_PARTITION_KEY,
                type=str,
                required=True,
            ),
        )
        _pk_constraint.fields.append(SECONDARY_PARTITION_KEY)

    for _, property_data in (object_schema.properties or {}).items():
        _property = glue.PropertySchema(
            name=property_data.field_name or '',
            type=object_schema_type_to_glue_type(property_data.type),
            required=property_data.field_name in object_schema.required,
            default=property_data.default,
            description=property_data.title,
        )
        _schema.properties.append(_property)

    for unique_fields in getattr(object_schema, 'unique', []) or []:
        if not _schema.constraints:
            _schema.constraints = []

        _schema.constraints.append(
            glue.UniqueConstraint(
                fields=unique_fields,
                name=f'unq_{object_schema.title.lower()}_{"_".join(unique_fields)}',
            ),
        )

    for indexed_field in getattr(object_schema, 'indexed', []) or []:
        if not _schema.indexes:
            _schema.indexes = []

        _schema.indexes.append(
            glue.IndexSchema(
                fields=[indexed_field],
                name=f'idx_{object_schema.title.lower()}_{indexed_field}',
            ),
        )

    return _schema


def object_schema_type_to_glue_type(property_type: str) -> glue.Schema | glue.SchemaReference | type[Any]:
    if property_type == CoreTypes.ANYTHING.value:
        return dict

    if property_type == CoreTypes.NUMBER.value:
        return float

    if property_type == CoreTypes.BOOLEAN.value:
        return bool

    if property_type == CoreTypes.STRING.value:
        return str

    if property_type == CoreTypes.DATE.value:
        return date

    if property_type == CoreTypes.DATETIME.value:
        return datetime

    if property_type == CoreTypes.BINARY.value:
        return bytes

    if property_type == CoreTypes.ARRAY.value:
        return list

    if property_type == CoreTypes.DICTIONARY.value:
        return dict

    if is_reference_type(property_type):
        return dict
    return str


def is_reference_type(property_type: str) -> bool:
    return property_type[0] == property_type[0].upper()
