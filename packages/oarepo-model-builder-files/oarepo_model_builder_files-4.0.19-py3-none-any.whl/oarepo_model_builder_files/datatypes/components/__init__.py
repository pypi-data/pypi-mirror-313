from .file import FileComponent
from .files_model import (
    FilesDefaultsModelComponent,
    FilesExtResourceModelComponent,
    FilesFieldModelComponent,
    FilesPermissionsModelComponent,
    FilesPIDModelComponent,
    FilesRecordMetadataModelComponent,
    FilesRecordModelComponent,
    FilesResourceModelComponent,
    FilesServiceModelComponent,
)
from .files_tests import FilesModelTestComponent
from .parent_record import ParentRecordComponent

file_components = [
    FileComponent,
    ParentRecordComponent,
    FilesFieldModelComponent,
    FilesModelTestComponent,
    FilesDefaultsModelComponent,
    FilesRecordModelComponent,
    FilesRecordMetadataModelComponent,
    FilesResourceModelComponent,
    FilesServiceModelComponent,
    FilesExtResourceModelComponent,
    FilesPermissionsModelComponent,
    FilesPIDModelComponent,
]
