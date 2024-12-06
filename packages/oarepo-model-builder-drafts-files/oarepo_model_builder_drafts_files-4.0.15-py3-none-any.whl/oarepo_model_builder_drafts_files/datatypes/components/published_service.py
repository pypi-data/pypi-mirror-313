from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder_drafts.datatypes.components import PublishedServiceComponent
from oarepo_model_builder_files.datatypes import FileDataType


class DraftFilesPublishedServiceComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [PublishedServiceComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile in {"record"}:
            config = set_default(datatype, "published-service-config", {})
            config.setdefault("components", [])
            config["components"] += [
                "{{oarepo_runtime.services.files.FilesComponent}}",
                "{{oarepo_published_service.services.records.components.bucket.CreatePublishedBucketComponent}}",
            ]


class FilesPublishedServiceComponent(PublishedServiceComponent):
    eligible_datatypes = [FileDataType]
    dependency_remap = PublishedServiceComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile in {"files"}:
            config = set_default(datatype, "published-service-config", {})
            service = set_default(datatype, "published-service", {})

            config.setdefault(
                "base-classes",
                [datatype.definition["service-config"]["class"]],
            )
            service.setdefault(
                "base-classes",
                ["invenio_records_resources.services.FileService"],
            )
            service.setdefault("proxy", "current_files_published_service")
            super().before_model_prepare(datatype, context=context, **kwargs)
