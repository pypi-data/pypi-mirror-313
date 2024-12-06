from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import (
    append_array,
    set_default,
)


class InvenioDraftsFilesRecordComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [
        ServiceModelComponent,
    ]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "record":
            append_array(
                datatype,
                "service-config",
                "components",
                "{{invenio_drafts_resources.services.records.components.DraftFilesComponent}}",
            )
            service = set_default(datatype, "service", {})
            service.setdefault("additional-args", {})
            service["additional-args"] += [
                f"files_service=self.service_files",
                f"draft_files_service=self.service_draft_files",
            ]
