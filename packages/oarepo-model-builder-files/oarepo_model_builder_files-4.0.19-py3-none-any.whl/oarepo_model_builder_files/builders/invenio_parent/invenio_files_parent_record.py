from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesParentRecordBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_parent_record"
    section = "record"
    template = "files-parent-record"
