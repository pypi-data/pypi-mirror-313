from oarepo_model_builder.datatypes import DataType, ModelDataType
from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class DraftServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = ServiceModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return
        record_service = set_default(datatype, "service", {})
        record_service_config = set_default(datatype, "service-config", {})

        if datatype.root.profile == "draft":
            published_record_datatype: DataType = context["published_record"]
            record_service.setdefault(
                "class", published_record_datatype.definition["service"]["class"]
            )
            record_service_config.setdefault(
                "class", published_record_datatype.definition["service-config"]["class"]
            )
            record_service_config.setdefault(
                "service-id",
                published_record_datatype.definition["service-config"]["service-id"],
            )

        if datatype.root.profile == "record":
            record_service.setdefault(
                "imports",
                [],
            )
            record_service.setdefault(
                "base-classes",
                [
                    "invenio_drafts_resources.services.RecordService{InvenioRecordService}"
                ],
            )
            record_service_config.setdefault(
                "base-classes",
                [
                    "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
                    "invenio_drafts_resources.services.RecordServiceConfig{InvenioRecordDraftsServiceConfig}",
                ],
            )

        super().before_model_prepare(datatype, context=context, **kwargs)
        record_service_config.setdefault("components", []).append(
            "{{oarepo_runtime.services.components.OwnersComponent}}"
        )
