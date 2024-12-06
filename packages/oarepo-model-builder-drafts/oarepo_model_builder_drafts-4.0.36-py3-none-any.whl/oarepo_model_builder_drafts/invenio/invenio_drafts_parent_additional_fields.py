from pathlib import Path

from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.python import PythonOutput


class InvenioDraftsParentAdditionalFieldsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_drafts_parent_additional_fields"
    section = "draft-parent-record"
    template = "drafts-parent-additional-fields"

    def finish(self, **extra_kwargs):
        super().finish(**extra_kwargs)

    def process_template(self, python_path: Path, template, **extra_kwargs):
        if self.parent_modules:
            self.create_parent_modules(python_path)
        output: PythonOutput = self.builder.get_output("python", python_path)
        context = dict(
            settings=self.settings,
            current_model=self.current_model,
            schema=self.current_model.schema.schema,
            **extra_kwargs,
        )
        output.merge(template, context)
