from oarepo_model_builder_files.builders.parent_builder import InvenioFilesParentBuilder


class InvenioFilesTestFileResourcesBuilder(InvenioFilesParentBuilder):
    TYPE = "invenio_files_test_files_resources"
    template = "files-test-file-resources"

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        files_tests = getattr(self.current_model, "section_files_tests")
        super().finish(
            fixtures=tests.fixtures | files_tests.fixtures,
            test_constants=tests.constants | files_tests.constants,
            **extra_kwargs,
        )

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.files.test_file_resources'
