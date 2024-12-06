from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsParentStateBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_parent_state"
    section = "draft-parent-record-state"
    template = "drafts-parent-state"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
