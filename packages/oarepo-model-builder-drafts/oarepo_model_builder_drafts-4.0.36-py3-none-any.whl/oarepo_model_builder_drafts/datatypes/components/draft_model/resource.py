from oarepo_model_builder.datatypes import DataType, ModelDataType
from oarepo_model_builder.datatypes.components import ResourceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class DraftResourceModelComponent(ResourceModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = ResourceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return
        record_resource = set_default(datatype, "resource", {})
        record_resource_config = set_default(datatype, "resource-config", {})

        if datatype.root.profile == "draft":
            published_record_datatype: DataType = context["published_record"]
            record_resource.setdefault(
                "class", published_record_datatype.definition["resource"]["class"]
            )
            record_resource_config.setdefault(
                "class",
                published_record_datatype.definition["resource-config"]["class"],
            )

        if datatype.root.profile == "record":
            record_resource.setdefault(
                "base-classes",
                ["invenio_drafts_resources.resources.RecordResource"],
            )
            record_resource_config.setdefault(
                "base-classes",
                ["invenio_drafts_resources.resources.RecordResourceConfig"],
            )

        super().before_model_prepare(datatype, context=context, **kwargs)
