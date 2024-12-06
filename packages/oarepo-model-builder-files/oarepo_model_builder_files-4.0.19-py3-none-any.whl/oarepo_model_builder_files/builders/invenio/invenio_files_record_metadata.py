from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesRecordMetadataBuilder(BaseBuilder):
    TYPE = "invenio_files_record_metadata"
    section = "record-metadata"
    template = "files-record-metadata"
