from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder_files.datatypes import FileDataType
from oarepo_model_builder_files.datatypes.components import FilesFieldModelComponent


class DraftFilesFieldModelComponent(FilesFieldModelComponent):
    eligible_datatypes = [FileDataType]
    depends_on = [RecordModelComponent]
    dependency_remap = FilesFieldModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"files", "draft_files"}:
            return
        files_field = set_default(datatype, "files-field", {})
        if datatype.root.profile == "draft_files":
            files_field.setdefault("file-class", datatype.definition["record"]["class"])
            files_field.setdefault("field-args", ["store=False", "delete=False"])
            # files_field.setdefault(
            #     "imports",
            #     [
            #         {
            #             "import": "invenio_records_resources.records.systemfields.FilesField"
            #         },
            #     ],
            # )

        if datatype.root.profile == "files":
            files_field.setdefault(
                "field-args", ["store=False", "create=False", "delete=False"]
            )

        super().before_model_prepare(datatype, context=context, **kwargs)
