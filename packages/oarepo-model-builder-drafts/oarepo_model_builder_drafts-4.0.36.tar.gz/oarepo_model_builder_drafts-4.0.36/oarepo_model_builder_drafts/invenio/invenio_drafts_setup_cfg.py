from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class InvenioDraftsSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_drafts_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        if not self.current_model.definition["published-service"].get("skip"):
            output.add_dependency("oarepo-published-service", ">=1.0.0")
