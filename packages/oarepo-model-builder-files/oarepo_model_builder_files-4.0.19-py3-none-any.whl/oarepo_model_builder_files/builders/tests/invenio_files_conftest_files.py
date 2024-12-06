from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesConftestFilesBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_conftest_files"
    template = "files-conftest"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.files.conftest'
