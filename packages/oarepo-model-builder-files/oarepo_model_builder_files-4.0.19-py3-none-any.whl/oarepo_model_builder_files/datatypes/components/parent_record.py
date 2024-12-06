from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    RecordMetadataModelComponent,
    ServiceModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import (
    append_array,
    prepend_array,
)


class ParentRecordComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [
        DefaultsModelComponent,
        RecordMetadataModelComponent,
        ServiceModelComponent,
    ]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if context["profile"] != "record":
            return
        # have files plugin in virtualenv but there are no files in the record
        if "files" not in datatype.definition:
            return
        prepend_array(
            datatype,
            "record-metadata",
            "base-classes",
            "invenio_records.models.RecordMetadataBase",
        )
        prepend_array(
            datatype, "record-metadata", "base-classes", "invenio_db.db{db.Model}"
        )

        append_array(
            datatype,
            "service-config",
            "components",
            "{{oarepo_runtime.services.files.FilesComponent}}",
        )
