from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsRecordExtraFieldsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_record_extra_fields"
    section = "record"
    template = "drafts-record-extra-fields"
    record_section = "section_record"

    def finish(self, **extra_kwargs):
        super().finish(
            record=getattr(self.current_model, self.record_section).config,
            **extra_kwargs,
        )
