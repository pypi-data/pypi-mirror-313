import marshmallow as ma
from oarepo_model_builder.datatypes import ModelDataType


class DraftDataType(ModelDataType):
    model_type = "draft_record"

    class ModelSchema(ModelDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="draft_record",
            required=False,
            validate=ma.validate.Equal("draft_record"),
        )
        extra_code = ma.fields.String(
            attribute="extra-code",
            data_key="extra-code",
            metadata={"doc": "Extra code to be copied below the permission class"},
        )
        generate = ma.fields.Boolean()
        skip = ma.fields.Boolean()

    def before_model_prepare(self, datatype, *, context, **kwargs):
        draft = set_default(datatype, "draft", {})
        draft.setdefault("generate", True)
        draft.setdefault("extra-code", "")

    def prepare(self, context):
        self.published_record = context["published_record"]
        super().prepare(context)
