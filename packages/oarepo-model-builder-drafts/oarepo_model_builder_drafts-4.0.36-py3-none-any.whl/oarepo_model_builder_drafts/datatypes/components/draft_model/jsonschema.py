from oarepo_model_builder.datatypes.components import JSONSchemaModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_drafts.datatypes import DraftDataType


class DraftJSONSchemaModelComponent(JSONSchemaModelComponent):
    eligible_datatypes = [DraftDataType]
    dependency_remap = JSONSchemaModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        published_datatype = context["published_record"].definition

        json_schema = set_default(datatype, "json-schema-settings", {})
        json_schema.setdefault(
            "alias", published_datatype["json-schema-settings"]["alias"]
        )

        json_schema.setdefault(
            "module",
            published_datatype["json-schema-settings"]["module"],
        )
        json_schema.setdefault(
            "name",
            published_datatype["json-schema-settings"]["name"],
        )

        json_schema.setdefault(
            "file",
            published_datatype["json-schema-settings"]["file"],
        )

        super().before_model_prepare(datatype, context=context, **kwargs)
