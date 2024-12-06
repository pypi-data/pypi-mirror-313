from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesRecordPermissionsBuilder(BaseBuilder):
    TYPE = "invenio_files_permissions"
    section = "permissions"
    template = "files-permissions"
