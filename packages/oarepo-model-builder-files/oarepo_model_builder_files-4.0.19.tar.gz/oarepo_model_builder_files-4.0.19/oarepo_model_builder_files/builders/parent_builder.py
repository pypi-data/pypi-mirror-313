from oarepo_model_builder_files.builders.base import BaseBuilder


class InvenioFilesParentBuilder(BaseBuilder):
    def _get_output_module(self):
        profile = self.current_model.root.profile
        if profile == "files":
            metadata_record = "published_record"
        elif profile == "draft_files":
            metadata_record = "draft_record"
        metadata_record = getattr(self.current_model, metadata_record)
        module = metadata_record.definition[self.section]["module"]
        return module
