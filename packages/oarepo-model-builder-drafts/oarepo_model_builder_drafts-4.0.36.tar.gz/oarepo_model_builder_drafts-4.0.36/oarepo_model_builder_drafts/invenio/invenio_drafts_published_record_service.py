from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsPublishedRecordServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_published_record_service"
    section = "published-service"
    template = "drafts-published-record-service"

    def finish(self, **extra_kwargs):
        return super().finish(**extra_kwargs)
