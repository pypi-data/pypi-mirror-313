from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import PIDModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesPIDModelComponent(PIDModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = PIDModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]

        pid = set_default(datatype, "pid", file_record_datatype.definition["pid"])
        for k, v in file_record_datatype.definition["pid"].items():
            pid.setdefault(k, v)
        super().before_model_prepare(datatype, context=context, **kwargs)
