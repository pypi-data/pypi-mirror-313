from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_files.datatypes import FileDataType


class FilesServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [FileDataType]
    dependency_remap = ServiceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):

        service_config = set_default(datatype, "service-config", {})
        service_config.setdefault(
            "base-classes",
            [
                "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
                "invenio_records_resources.services.FileServiceConfig",
            ],
        )
        service_config.setdefault("imports", [])
        allowed_mimetypes = datatype.definition.get('allowed-mimetypes', [])
        allowed_extensions = datatype.definition.get('allowed-extensions', [])
        service_config.setdefault("mimetypes", allowed_mimetypes)
        service_config.setdefault("extensions", allowed_extensions)
        service = set_default(datatype, "service", {})
        service.setdefault(
            "base-classes", ["invenio_records_resources.services.FileService"]
        )
        service.setdefault("imports", [])
        super().before_model_prepare(datatype, context=context, **kwargs)
