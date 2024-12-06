from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesDefaultsModelComponent(DefaultsModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = DefaultsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        parent_file_record_prefix = file_record_datatype.definition["module"]["prefix"]
        parent_file_record_alias = file_record_datatype.definition["module"]["alias"]

        module = set_default(datatype, "module", {})
        module.setdefault(
            "qualified", file_record_datatype.definition["module"]["qualified"]
        )
        module.setdefault("prefix", f"{parent_file_record_prefix}Draft")
        module.setdefault("alias", f"{parent_file_record_alias}_draft")

        super().before_model_prepare(datatype, context=context, **kwargs)
