from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsPublishedRecordServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_published_record_service_config"
    section = "published-service-config"
    template = "drafts-published-record-service-config"
