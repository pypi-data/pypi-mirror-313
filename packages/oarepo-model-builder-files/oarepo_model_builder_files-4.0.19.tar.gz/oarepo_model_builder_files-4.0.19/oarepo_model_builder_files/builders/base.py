from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class BaseBuilder(InvenioBaseClassPythonBuilder):
    def finish(self, **extra_kwargs):
        profile = self.current_model.root.profile
        if profile == "files":
            metadata_record = "published_record"
        elif profile == "draft_files":
            metadata_record = "draft_record"
        metadata_record = getattr(self.current_model, metadata_record)
        metadata_record = metadata_record.definition
        super().finish(metadata_record=metadata_record, **extra_kwargs)
