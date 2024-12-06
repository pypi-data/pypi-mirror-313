from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsHasDraftCheckfieldBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_has_draft_checkfield"
    section = "record"
    template = "drafts-has-draft-checkfield"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
