from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder_tests.datatypes.components import ModelTestComponent


class FilesModelTestComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ModelTestComponent]

    def process_files_tests(self, datatype, section, **extra_kwargs):
        section.fixtures = {}
        section.constants = {
            "skip_continous_disable_files_test": False,
            "files_base_url_placeholder": "base_files_url",
            "links_record_files": {
                "self": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files",
            },
            "links_files": {
                "self": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf",
                "content": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/content",
                "commit": "https://{site_hostname}/api{base_files_url.replace('{id}', id_)}/files/test.pdf/commit",
            },
        }
