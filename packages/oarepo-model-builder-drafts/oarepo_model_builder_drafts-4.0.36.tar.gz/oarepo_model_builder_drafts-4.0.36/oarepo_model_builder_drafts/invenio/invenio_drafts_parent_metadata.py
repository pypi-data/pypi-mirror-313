from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsParentMetadataBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_parent_metadata"
    section = "draft-parent-record-metadata"
    template = "drafts-parent-metadata"
