from pathlib import Path
from typing import List, Union

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.profiles.record import RecordProfile
from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.utils.dict import dict_get


class DraftProfile(RecordProfile):
    default_model_path = ["record", "draft"]

    def build(
        self,
        model: ModelSchema,
        profile: str,
        model_path: List[str],
        output_directory: Union[str, Path],
        builder: ModelBuilder,
        **kwargs,
    ):
        published_record = model.get_schema_section("record", model_path[:-1])
        if not dict_get(model.schema, model_path):
            return
        draft_profile = dict_get(model.schema, model_path)
        draft_profile["type"] = "draft_record"

        # pass the parent record as an extra context item. This will be handled by file-aware
        # components in their "prepare" method
        super().build(
            model=model,
            profile=profile,
            model_path=model_path,
            output_directory=output_directory,
            builder=builder,
            context={
                "profile": "draft",
                "profile_module": "records",
                "published_record": published_record,
            },
        )
