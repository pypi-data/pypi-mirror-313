from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesParentRecordMetadataBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_parent_record_metadata"
    section = "record-metadata"
    template = "files-parent-record-metadata"
