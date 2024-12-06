from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsRecordMetadataExtraFieldsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_record_metadata_extra_fields"
    section = "record-metadata"
    template = "drafts-record-metadata-extra-fields"
    record_metadata_section = "section_record_metadata"

    def finish(self, **extra_kwargs):
        super().finish(
            record_metadata=getattr(
                self.current_model, self.record_metadata_section
            ).config,
            **extra_kwargs,
        )
