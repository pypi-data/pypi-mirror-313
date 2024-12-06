from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import RecordMetadataModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder_files.datatypes.components import (
    FilesRecordMetadataModelComponent,
)

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesRecordMetadataModelComponent(FilesRecordMetadataModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = RecordMetadataModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        parent_file_record_prefix = file_record_datatype.definition["module"]["prefix"]
        draft_file_record = set_default(datatype, "record", {})
        draft_file_record.setdefault("class", f"{parent_file_record_prefix}Draft")
        super().before_model_prepare(datatype, context=context, **kwargs)
