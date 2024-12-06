import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    MarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.validation.utils import ImportSchema


class ParentMarshmallowClassSchema(ma.Schema):
    module = ma.fields.String(metadata={"doc": "Class module"})
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "base classes"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class ParentMarshmallowComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, MarshmallowModelComponent]

    class ModelSchema(ma.Schema):
        parent_record_marshmallow = ma.fields.Nested(
            ParentMarshmallowClassSchema,
            attribute="parent-record-marshmallow",
            data_key="parent-record-marshmallow",
        )

    def process_mb_invenio_drafts_parent_marshmallow(self, datatype, section, **kwargs):
        obj = section.config.setdefault("additional-fields", {})
        obj |= {"owners": "ma.fields.List(ma.fields.Dict(), load_only=True)"}

    def before_model_prepare(self, datatype, *, context, **kwargs):
        marshmallow = set_default(datatype, "parent-record-marshmallow", {})
        m_module = marshmallow.setdefault(
            "module", datatype.definition["marshmallow"]["module"]
        )
        marshmallow.setdefault("class", f"{m_module}.GeneratedParentSchema")
        marshmallow.setdefault("generate", True)
        marshmallow.setdefault(
            "base-classes",
            [
                "invenio_drafts_resources.services.records.schema.ParentSchema{InvenioParentSchema}"
            ],
        )
