from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import PIDModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class DraftPIDModelComponent(PIDModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = PIDModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return

        pid = set_default(datatype, "pid", {})
        pid.setdefault(
            "provider-base-classes",
            ["invenio_drafts_resources.records.api.DraftRecordIdProviderV2"],
        )
        pid.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDField"
                },
                {
                    "import": "invenio_records_resources.records.systemfields.pid.PIDFieldContext"
                },
                # {
                #     "import": "invenio_drafts_resources.records.api.DraftRecordIdProviderV2"
                # },
            ],
        )
        if datatype.root.profile == "draft":
            published = context["published_record"]
            pid = set_default(datatype, "pid", {})
            pid.setdefault(
                "provider-class",
                published.definition["pid"]["provider-class"],
            )
            pid.setdefault("field-args", ["create=True", "delete=False"])

        super().before_model_prepare(datatype, context=context, **kwargs)
