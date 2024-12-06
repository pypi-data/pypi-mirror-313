from oarepo_model_builder.datatypes.components import PIDModelComponent
from oarepo_model_builder.datatypes.components.model.pid import process_pid_type
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_files.datatypes import FileDataType

from ..utils import get_metadata_record


class FilesPIDModelComponent(PIDModelComponent):
    eligible_datatypes = [FileDataType]
    dependency_remap = PIDModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        pid = set_default(datatype, "pid", {})
        parent_record_datatype = get_metadata_record(datatype, context)
        pid.setdefault(
            "type",
            process_pid_type(parent_record_datatype.definition["pid"]["type"] + "File"),
        )
        super().before_model_prepare(datatype, context=context, **kwargs)
