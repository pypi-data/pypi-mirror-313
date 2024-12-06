from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsParentMarshmallowLinkBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_parent_marshmallow_link"
    section = "marshmallow"
    template = "drafts-parent-marshmallow-link"
