from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_config"
    section = "config"
    template = "drafts-config"
