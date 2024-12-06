from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles.record import RecordProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class DraftFilesProfile(RecordProfile):
    default_model_path = ["record", "draft-files"]

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        # get parent record. In most cases, it has already been prepared and is reused
        # from cache. It files profile is called the first, then this will call prepare({})
        # on the record and will take some time (no files will be generated, only class names
        # allocated)
        draft_record = model.get_schema_section("draft", model_path[:-1] + ["draft"])
        file_record = model.get_schema_section("files", model_path[:-1] + ["files"])
        parent_record = model.get_schema_section("record", model_path[:-1])

        draft_file_profile = dict_get(model.schema, model_path)
        draft_file_profile.setdefault("type", "draft_files")

        # pass the parent record as an extra context item. This will be handled by file-aware
        # components in their "prepare" method
        super().build(
            model=model,
            profile=profile,
            model_path=model_path,
            output_directory=output_directory,
            builder=builder,
            context={
                "draft_record": draft_record,
                "file_record": file_record,
                "parent_record": parent_record,
                "profile": "draft_files",
                "profile_module": "files",
                "switch_profile": True,
            },
        )


"""
class DraftsFilesProfile(Profile):

    def build(
            self,
            model: ModelSchema,
            output_directory: Union[str, Path],
            builder: ModelBuilder,
    ):
        original_model_preprocessors = [model_preprocessor for model_preprocessor in builder.model_preprocessor_classes
                                        if "oarepo_model_builder." in str(model_preprocessor)]
        builder._validate_model(model)
        for model_preprocessor in original_model_preprocessors:
            model_preprocessor(builder).transform(model, model.settings)

        model.model_field = "files"
        builder.build(model, output_directory)
"""
