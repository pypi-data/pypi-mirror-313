from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioDraftsTestResourcesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_test_resources"
    template = "drafts-test-resources"
    MODULE = "tests.test_resources"

    def _get_output_module(self):
        return f'{self.current_model.definition["tests"]["module"]}.test_resource'

    def finish(self, **extra_kwargs):
        tests = getattr(self.current_model, "section_tests")
        add_fields = getattr(self.current_model, "section_draft_parent_record")
        super().finish(
            fixtures=tests.fixtures,
            test_constants=tests.constants,
            published_record=self.current_model.published_record,
            **extra_kwargs,
        )
