from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class FilesServiceConfigDisableUploadBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "files_service_config_disable_upload"
    section = "service-config"
    template = "service-config-disable-upload"
