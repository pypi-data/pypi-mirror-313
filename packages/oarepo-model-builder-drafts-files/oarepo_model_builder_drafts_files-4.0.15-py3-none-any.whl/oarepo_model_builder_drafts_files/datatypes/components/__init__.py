from .draft_file_model import (
    DraftFilesBlueprintsModelComponent,
    DraftFilesDefaultsModelComponent,
    DraftFilesExtResourceModelComponent,
    DraftFilesFieldModelComponent,
    DraftFilesMarshmallowModelComponent,
    DraftFilesParentComponent,
    DraftFilesPIDModelComponent,
    DraftFilesRecordMetadataModelComponent,
    DraftFilesRecordModelComponent,
    DraftFilesResourceModelComponent,
    DraftFilesServiceModelComponent,
)
from .draft_file_profile import DraftFileComponent
from .draft_files_tests import (
    DraftFilesFilesModelTestComponent,
    DraftFilesModelTestComponent,
)
from .drafts_files_record import InvenioDraftsFilesRecordComponent
from .published_service import (
    DraftFilesPublishedServiceComponent,
    FilesPublishedServiceComponent,
)

DRAFTS_FILES_COMPONENTS = [
    DraftFilesFieldModelComponent,
    DraftFileComponent,
    InvenioDraftsFilesRecordComponent,
    DraftFilesModelTestComponent,
    DraftFilesFilesModelTestComponent,
    DraftFilesDefaultsModelComponent,
    DraftFilesMarshmallowModelComponent,
    DraftFilesRecordModelComponent,
    DraftFilesRecordMetadataModelComponent,
    DraftFilesResourceModelComponent,
    DraftFilesServiceModelComponent,
    DraftFilesPIDModelComponent,
    DraftFilesBlueprintsModelComponent,
    DraftFilesExtResourceModelComponent,
    DraftFilesParentComponent,
    DraftFilesPublishedServiceComponent,
    FilesPublishedServiceComponent,
]
