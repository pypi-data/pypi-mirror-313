from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioExtPublishedServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ext_published_service"
    section = "ext"
    template = "drafts-published-ext-service"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_ext_resource.config
        published_service = self.current_model.section_published_service.config
        published_service_config = (
            self.current_model.section_published_service_config.config
        )

        super().finish(
            ext=ext,
            published_service=published_service,
            published_service_config=published_service_config,
            **extra_kwargs,
        )
