from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsParentMarshmallowBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_parent_marshmallow"
    section = "marshmallow"
    template = "drafts-parent-marshmallow"
