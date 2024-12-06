import marshmallow as ma
from oarepo_model_builder.datatypes import ModelDataType


class FileDataType(ModelDataType):
    model_type = "file"

    class ModelSchema(ModelDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="file",
            required=False,
            validate=ma.validate.Equal("file"),
        )

    def prepare(self, context):
        self.published_record = context["published_record"]
        super().prepare(context)
