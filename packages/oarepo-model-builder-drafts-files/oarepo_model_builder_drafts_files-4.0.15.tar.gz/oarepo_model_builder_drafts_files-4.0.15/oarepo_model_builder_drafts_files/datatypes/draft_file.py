import marshmallow as ma
from oarepo_model_builder.datatypes import ModelDataType


class DraftFileDataType(ModelDataType):
    model_type = "draft-file"

    class ModelSchema(ModelDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="draft-file",
            required=False,
            validate=ma.validate.Equal("draft-file"),
        )

    def prepare(self, context):
        self.draft_record = context["draft_record"]
        self.file_record = context["file_record"]
        super().prepare(context)
