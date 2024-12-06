from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesRecordBuilder(BaseBuilder):
    TYPE = "invenio_files_record"
    section = "record"
    template = "files-record"
