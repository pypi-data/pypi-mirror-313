from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.python_name import package_name


class InvenioDraftsRecordCommunitiesServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_record_communities_service_config"
    section = "service-config"
    template = "drafts-record-communities-service-config"

    def _get_output_module(self):
        module = package_name(self.vars["record-communities-service-config"]["class"])
        return module

    def finish(self, **extra_kwargs):
        vars = self.vars
        if "record-communities-service-config" not in vars:
            return
        super().finish(**extra_kwargs)
