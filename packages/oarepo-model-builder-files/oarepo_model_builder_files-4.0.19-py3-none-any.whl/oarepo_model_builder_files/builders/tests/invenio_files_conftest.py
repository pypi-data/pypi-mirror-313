from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesConftestBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_conftest"
    template = "files-top-conftest"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.conftest'
