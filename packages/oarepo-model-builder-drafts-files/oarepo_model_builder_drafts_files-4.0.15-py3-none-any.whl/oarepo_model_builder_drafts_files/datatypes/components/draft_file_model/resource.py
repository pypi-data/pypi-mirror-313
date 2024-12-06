from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import ResourceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder_files.datatypes.components import FilesResourceModelComponent

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesResourceModelComponent(FilesResourceModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = ResourceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        resource_config = set_default(datatype, "resource-config", {})
        file_record_url = file_record_datatype.definition["resource-config"]["base-url"]
        resource_config.setdefault("base-url", f"{file_record_url}/draft")
        super().before_model_prepare(datatype, context=context, **kwargs)
