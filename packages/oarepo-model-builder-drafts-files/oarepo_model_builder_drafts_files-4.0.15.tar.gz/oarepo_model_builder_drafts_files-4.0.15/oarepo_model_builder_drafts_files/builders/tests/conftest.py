from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class ConftestBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_drafts_conftest"
    template = "draft-files-conftest"

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        super().finish(
            file_record=self.current_model.file_record.definition,
            test_constants=tests.constants,
            **extra_kwargs,
        )

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.conftest'
