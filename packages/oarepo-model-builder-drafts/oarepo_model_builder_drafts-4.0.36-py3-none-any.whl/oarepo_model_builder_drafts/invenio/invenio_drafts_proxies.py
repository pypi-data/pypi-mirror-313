from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsProxiesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_proxies"
    section = "proxy"
    template = "drafts-proxies"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_published_service.config
        super().finish(ext=ext, **extra_kwargs)
