from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder_drafts.datatypes.components import DraftModelTestComponent
from oarepo_model_builder_files.datatypes.components import FilesModelTestComponent


class DraftFilesModelTestComponent(DraftModelTestComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = DraftModelTestComponent

    def process_tests(self, datatype, section, **extra_kwargs):
        super().process_tests(datatype, section, **extra_kwargs)
        # the DraftFilesComponent setting enabled=false on original draft tests increases revision id
        # this is probably due to db revert of bucket identifiers?
        # disabling bucket fields in models prevents the change
        section.constants["revision_id1"] = 3
        section.constants["revision_id2"] = 8
        section.constants["revision_id3"] = 13

        section.constants["links_record_files"] = {
            "self": "https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files",
        }

        section.constants["links_files"] = {
            "self": "https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf",
            "content": "https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf/content",
            "commit": "https://{site_hostname}/api{base_urls['base_files_url'].replace('{id}', id_)}/files/test.pdf/commit",
        }


class DraftFilesFilesModelTestComponent(FilesModelTestComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = FilesModelTestComponent

    def process_files_tests(self, datatype, section, **extra_kwargs):
        super().process_files_tests(datatype, section, **extra_kwargs)
        section.constants["skip_continous_disable_files_test"] = True
        section.constants["links_record_files"][
            "self"
        ] = "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files"
        section.constants["files_base_url_placeholder"] = "base_draft_files_url"
        section.constants["links_files"] = {
            "self": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf",
            "content": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/content",
            "commit": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/commit",
        }
