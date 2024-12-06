import copy

from oarepo_model_builder.datatypes import ModelDataType, datatypes
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    JSONSchemaModelComponent,
    MappingModelComponent,
    RecordModelComponent,
)


class DraftMappingModelComponent(MappingModelComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [
        DefaultsModelComponent,
        RecordModelComponent,
        JSONSchemaModelComponent,
    ]
    dependency_remap = MappingModelComponent

    def process_mapping(self, datatype, section, **kwargs):
        if datatype.root.profile == "draft":
            section.children["expires_at"] = datatypes.get_datatype(
                datatype,
                {
                    "type": "datetime",
                    "sample": {"skip": True},
                    "marshmallow": {"read": False, "write": False},
                    "ui": {"marshmallow": {"read": False, "write": False}},
                },
                "expires_at",
                datatype.model,
                datatype.schema,
            )
            section.children["expires_at"].prepare(context={})
            section.children["fork_version_id"] = datatypes.get_datatype(
                datatype,
                {
                    "type": "integer",
                    "sample": {"skip": True},
                    "marshmallow": {"read": False, "write": False},
                    "ui": {"marshmallow": {"read": False, "write": False}},
                },
                "fork_version_id",
                datatype.model,
                datatype.schema,
            )
            section.children["fork_version_id"].prepare(context={})

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "record" and "mapping" in datatype.definition:
            self.mapping_default = copy.deepcopy(datatype.definition["mapping"])

        if datatype.root.profile == "draft" and hasattr(self, "mapping_default"):
            mapping = datatype.definition.get("mapping", {}) | self.mapping_default
            datatype.definition["mapping"] = mapping

        super().before_model_prepare(datatype, context=context, **kwargs)
        if datatype.root.profile == "draft":
            mapping = datatype.definition["mapping"]
            mapping_alias = datatype.definition["mapping"]["alias"]
            mapping.setdefault("index-field-args", []).append(
                f'search_alias="{mapping_alias}"'
            )
