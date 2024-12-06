from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import RecordDumperModelComponent


class DraftsRecordDumperModelComponent(RecordDumperModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = RecordDumperModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        super().before_model_prepare(datatype, context=context, **kwargs)
        if datatype.root.profile in {"record", "draft"}:
            ext_class = (
                "oarepo_runtime.records.systemfields.mapping.SystemFieldDumperExt"
            )
            datatype.definition["record-dumper"]["extensions"].append(
                "{{" + ext_class + "}}()"
            )
