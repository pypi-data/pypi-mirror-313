from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import MarshmallowModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesMarshmallowModelComponent(MarshmallowModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = MarshmallowModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        ma = set_default(datatype, "marshmallow", {})
        ma.setdefault("class", file_record_datatype.definition["marshmallow"]["class"])
        super().before_model_prepare(datatype, context=context, **kwargs)
