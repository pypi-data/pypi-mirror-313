import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.ext_resource import (
    ExtResourceSchema,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default


class DraftFilesExtResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        ext_resource = ma.fields.Nested(
            ExtResourceSchema,
            attribute="ext-resource",
            data_key="ext-resource",
        )

    def process_ext_resource(self, datatype, section, **kwargs):
        if datatype.root.profile == "draft_files":
            cfg = section.config
            cfg["ext-service-name"] = "service_draft_files"
            cfg["ext-resource-name"] = "resource_draft_files"

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if not datatype.root.profile == "draft_files":
            return
        ext = set_default(datatype, "ext-resource", {})

        ext.setdefault("generate", True)
        ext.setdefault("skip", False)
