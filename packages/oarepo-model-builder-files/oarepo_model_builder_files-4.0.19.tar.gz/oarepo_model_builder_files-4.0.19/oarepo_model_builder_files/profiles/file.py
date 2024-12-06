from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles.record import RecordProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class FileProfile(RecordProfile):
    default_model_path = ["record", "files"]

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        # get parent record. In most cases, it has already been prepared and is reused
        # from cache. It files profile is called the first, then this will call prepare({})
        # on the record and will take some time (no files will be generated, only class names
        # allocated)
        parent_record = model.get_schema_section("record", model_path[:-1])
        if "files" not in parent_record.definition:
            return

        file_profile = dict_get(model.schema, model_path)
        file_profile.setdefault("type", "file")

        # pass the parent record as an extra context item. This will be handled by file-aware
        # components in their "prepare" method
        super().build(
            model=model,
            profile=profile,
            model_path=model_path,
            output_directory=output_directory,
            builder=builder,
            context={
                "published_record": parent_record,
                "profile": "files",
                "profile_module": "files",
            },
        )
