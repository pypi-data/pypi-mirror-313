from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder_files.datatypes.components import FilesRecordModelComponent

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesRecordModelComponent(FilesRecordModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = RecordModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        parent_file_record_prefix = file_record_datatype.definition["module"][
            "prefix"
        ]  # todo use section here?
        draft_file_record = set_default(datatype, "record", {})
        draft_file_record.setdefault("class", f"{parent_file_record_prefix}Draft")
        super().before_model_prepare(datatype, context=context, **kwargs)
