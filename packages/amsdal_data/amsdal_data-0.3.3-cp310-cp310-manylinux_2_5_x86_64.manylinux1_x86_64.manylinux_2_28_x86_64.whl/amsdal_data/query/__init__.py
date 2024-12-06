import amsdal_glue as glue
from amsdal_utils.classes.metadata_manager import MetadataInfoQueryBase
from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.enums import Versions

from amsdal_data.application import DataApplication
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.errors import MetadataInfoQueryError


class MetadataInfoQuery(MetadataInfoQueryBase):
    @classmethod
    def get_reference_to(cls, metadata: Metadata) -> list[Reference]:
        object_version = metadata.address.object_version

        if object_version == Versions.LATEST:
            res = DataApplication().operation_manager.query_lakehouse(
                statement=glue.QueryStatement(
                    table=glue.SchemaReference(
                        name=metadata.address.class_name,
                        version=metadata.address.class_version,
                    ),
                    where=glue.Conditions(
                        glue.Condition(
                            field=glue.FieldReference(
                                field=cls._build_nested_field('object_id'),
                                table_name='t2',
                            ),
                            lookup=glue.FieldLookup.EQ,
                            value=glue.Value(metadata.address.object_id),
                        ),
                        glue.Condition(
                            field=glue.FieldReference(
                                field=cls._build_nested_field('next_version'),
                                table_name='t2',
                            ),
                            lookup=glue.FieldLookup.ISNULL,
                            value=glue.Value(True),
                        ),
                    ),
                ),
            )
            if not res.success or not res.data:
                msg = f'Failed to get references to: {res.message}'
                raise MetadataInfoQueryError(msg) from res.exception

            object_version = res.data[0].data['range_key']

        result = DataApplication().operation_manager.query_lakehouse(
            statement=glue.QueryStatement(
                table=glue.SchemaReference(
                    name=REFERENCE_TABLE,
                    version=glue.Version.LATEST,
                ),
                where=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=cls._build_nested_field('from_address__class_name'),
                            table_name=REFERENCE_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(metadata.address.class_name),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=cls._build_nested_field('from_address__object_id'),
                            table_name=REFERENCE_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(metadata.address.object_id),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=cls._build_nested_field('from_address__object_version'),
                            table_name=REFERENCE_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(object_version),
                    ),
                ),
            ),
        )
        if not result.success:
            msg = f'Failed to get references to: {result.message}'
            raise MetadataInfoQueryError(msg) from result.exception

        return [Reference(**{'ref': item.data['to_address']}) for item in (result.data or [])]

    @staticmethod
    def _build_nested_field(field: str) -> glue.Field:
        parts = field.split('__')
        root = glue.Field(name=parts[0])
        _parent = root

        for _part in parts[1:]:
            _child = glue.Field(name=_part, parent=_parent)
            _parent.child = _child
            _parent = _child

        return root

    @classmethod
    def get_referenced_by(cls, metadata: Metadata) -> list[Reference]:
        version_q = glue.Conditions(
            glue.Condition(
                field=glue.FieldReference(
                    field=cls._build_nested_field('to_address__object_version'),
                    table_name=REFERENCE_TABLE,
                ),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(metadata.address.object_version),
            ),
        )

        if metadata.is_latest:
            version_q |= glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=cls._build_nested_field('to_address__object_version'),
                        table_name=REFERENCE_TABLE,
                    ),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(True),
                ),
                glue.Condition(
                    field=glue.FieldReference(
                        field=cls._build_nested_field('to_address__object_version'),
                        table_name=REFERENCE_TABLE,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(Versions.LATEST.value),
                ),
                connector=glue.FilterConnector.OR,
            )

        result = DataApplication().operation_manager.query_lakehouse(
            statement=glue.QueryStatement(
                table=glue.SchemaReference(
                    name=REFERENCE_TABLE,
                    version=glue.Version.LATEST,
                ),
                where=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=cls._build_nested_field('to_address__class_name'),
                            table_name=REFERENCE_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(metadata.address.class_name),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=cls._build_nested_field('to_address__object_id'),
                            table_name=REFERENCE_TABLE,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(metadata.address.object_id),
                    ),
                    version_q,
                ),
            ),
        )

        if not result.success:
            msg = f'Failed to get references to: {result.message}'
            raise MetadataInfoQueryError(msg) from result.exception

        return [Reference(**{'ref': item.data['from_address']}) for item in (result.data or [])]
