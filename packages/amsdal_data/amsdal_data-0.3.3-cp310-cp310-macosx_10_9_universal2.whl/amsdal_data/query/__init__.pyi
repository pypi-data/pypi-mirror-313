import amsdal_glue as glue
from amsdal_data.application import DataApplication as DataApplication
from amsdal_data.connections.constants import REFERENCE_TABLE as REFERENCE_TABLE
from amsdal_data.errors import MetadataInfoQueryError as MetadataInfoQueryError
from amsdal_utils.classes.metadata_manager import MetadataInfoQueryBase
from amsdal_utils.models.data_models.metadata import Metadata as Metadata
from amsdal_utils.models.data_models.reference import Reference

class MetadataInfoQuery(MetadataInfoQueryBase):
    @classmethod
    def get_reference_to(cls, metadata: Metadata) -> list[Reference]: ...
    @staticmethod
    def _build_nested_field(field: str) -> glue.Field: ...
    @classmethod
    def get_referenced_by(cls, metadata: Metadata) -> list[Reference]: ...
