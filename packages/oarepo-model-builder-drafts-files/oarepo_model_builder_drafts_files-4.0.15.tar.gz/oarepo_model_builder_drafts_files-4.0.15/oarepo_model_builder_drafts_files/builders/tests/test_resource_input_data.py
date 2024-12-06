from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class TestResourceInputDataBuilder(InvenioFilesParentBuilder):
    TYPE = "test_resource_input_data"
    template = "test-resource-input-data"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.test_resource'
