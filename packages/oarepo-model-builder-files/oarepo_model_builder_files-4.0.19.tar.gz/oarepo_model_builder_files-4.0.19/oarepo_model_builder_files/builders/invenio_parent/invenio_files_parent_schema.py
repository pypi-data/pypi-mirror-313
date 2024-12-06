from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesParentSchemaBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_parent_schema"
    section = "marshmallow"
    template = "files-parent-schema"
