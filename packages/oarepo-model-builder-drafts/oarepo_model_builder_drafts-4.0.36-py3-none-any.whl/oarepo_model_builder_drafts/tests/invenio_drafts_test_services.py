from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsTestServicesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_test_services"
    template = "drafts-test-services"
    MODULE = "tests.test_services"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.test_service'

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        super().finish(
            fixtures=tests.fixtures,
            test_constants=tests.constants,
            published_record=self.current_model.published_record,
            **extra_kwargs,
        )
