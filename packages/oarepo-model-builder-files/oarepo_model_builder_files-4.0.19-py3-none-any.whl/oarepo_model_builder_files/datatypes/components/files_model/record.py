from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_files.datatypes import FileDataType

from ..utils import get_metadata_record


class FilesRecordModelComponent(RecordModelComponent):
    eligible_datatypes = [FileDataType]
    dependency_remap = RecordModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        parent_record_datatype = get_metadata_record(datatype, context)
        parent_record_prefix = parent_record_datatype.definition["module"]["prefix"]

        record = set_default(datatype, "record", {})
        record.setdefault("class", f"{parent_record_prefix}File")
        record.setdefault(
            "base-classes", ["invenio_records_resources.records.api.FileRecord"]
        )
        record.setdefault("imports", [])
        super().before_model_prepare(datatype, context=context, **kwargs)
