from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.components import BlueprintsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_drafts_files.datatypes import DraftFileDataType


class DraftFilesBlueprintsModelComponent(BlueprintsModelComponent):
    eligible_datatypes = [DraftFileDataType]
    dependency_remap = BlueprintsModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        file_record_datatype: DataType = context["file_record"]
        api = set_default(datatype, "api-blueprint", {})
        api.setdefault(
            "module",
            f"{file_record_datatype.definition['module']['qualified']}.views.{context['profile']}.api",
        )
        app = set_default(datatype, "app-blueprint", {})
        app.setdefault(
            "module",
            f"{file_record_datatype.definition['module']['qualified']}.views.{context['profile']}.app",
        )

        super().before_model_prepare(datatype, context=context, **kwargs)
