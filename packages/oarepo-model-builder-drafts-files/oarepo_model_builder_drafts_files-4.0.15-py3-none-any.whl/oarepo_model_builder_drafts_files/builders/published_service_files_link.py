from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class PublishedServiceFilesLinkBuilder(InvenioFilesParentBuilder):
    TYPE = "published_service_files_link"
    section = "published-service"
    template = "published-service-files-link"
