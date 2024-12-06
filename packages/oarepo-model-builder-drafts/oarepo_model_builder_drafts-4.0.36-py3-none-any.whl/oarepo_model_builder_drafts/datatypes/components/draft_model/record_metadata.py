from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components.model.record_metadata import (
    RecordMetadataModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import (
    place_after,
    set_default,
)


class DraftRecordMetadataModelComponent(RecordMetadataModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = RecordMetadataModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        draft_metadata = set_default(datatype, "record-metadata", {})
        if datatype.root.profile in {"record", "draft"}:
            if datatype.root.profile == "draft":
                draft_metadata.setdefault(
                    "base-classes",
                    [
                        "invenio_db.db{db.Model}",
                        "invenio_drafts_resources.records.DraftMetadataBase",
                        "invenio_drafts_resources.records.ParentRecordMixin",
                    ],
                )
                draft_metadata.setdefault(
                    "imports",
                    [],
                )
                draft_metadata.setdefault("use-versioning", False)

            super().before_model_prepare(datatype, context=context, **kwargs)

            place_after(
                datatype,
                "record-metadata",
                "base-classes",
                "invenio_records.models.RecordMetadataBase",
                "invenio_drafts_resources.records.ParentRecordMixin",
            )
