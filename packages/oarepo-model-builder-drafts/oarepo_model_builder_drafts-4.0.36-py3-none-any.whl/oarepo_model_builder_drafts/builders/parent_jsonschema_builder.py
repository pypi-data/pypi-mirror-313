from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.utils.dict import dict_get


class JSONSchemaDraftsParentBuilder(JSONSchemaBuilder):
    TYPE = "jsonschema_drafts_parent"
    output_file_type = "jsonschema"
    output_file_name = ["draft-parent-record-schema", "file"]
    parent_module_root_name = "jsonschemas"

    def builtin_json(self):
        return {
            "type": "object",
            "properties": {
                "$schema": {"type": "keyword"},
                "created": {"type": "datetime"},
                "id": {"type": "keyword"},
                "updated": {"type": "datetime"},
            },
        }

    def build_node(self, node):
        from oarepo_model_builder.datatypes import datatypes

        json = self.builtin_json()
        parsed_section = datatypes.get_datatype(
            parent=None,
            data=json,
            key=None,
            model=json,
            schema=json,
        )
        parsed_section.prepare({})
        skip = dict_get(
            self.current_model.definition, ["json-schema-settings", "skip"], False
        )
        if skip:
            return
        generated = self.generate(parsed_section)
        self.output.merge(generated)
