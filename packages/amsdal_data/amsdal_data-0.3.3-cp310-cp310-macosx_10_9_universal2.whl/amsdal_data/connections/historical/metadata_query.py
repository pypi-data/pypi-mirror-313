import amsdal_glue as glue

from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD


def build_metadata_query(object_id: str, *, is_class_meta: bool = False) -> glue.QueryStatement:
    return glue.QueryStatement(
        table=glue.SubQueryStatement(
            alias='m',
            query=glue.QueryStatement(
                table=glue.SchemaReference(name=METADATA_TABLE, version=glue.Version.LATEST),
                only=[glue.FieldReference(field=glue.Field(name='*'), table_name=METADATA_TABLE)],
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
                                            table_name=METADATA_TABLE,
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
                                            table_name=METADATA_TABLE,
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
                where=glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name='class_meta_schema_reference'),
                            table_name=METADATA_TABLE,
                        ),
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=not is_class_meta),
                    ),
                ),
            ),
        ),
        where=glue.Conditions(
            glue.Condition(
                field=glue.FieldReference(field=glue.Field(name='object_id'), table_name='m'),
                lookup=glue.FieldLookup.EQ,
                value=glue.Value(object_id),
            ),
            glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name=NEXT_VERSION_FIELD), table_name='m'),
                    lookup=glue.FieldLookup.ISNULL,
                    value=glue.Value(True),
                ),
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name=NEXT_VERSION_FIELD), table_name='m'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(''),
                ),
                connector=glue.FilterConnector.OR,
            ),
        ),
    )
