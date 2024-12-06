import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.datatypes.components import ExtResourceModelComponent
from oarepo_model_builder.datatypes.components.model import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.model import ModelDataType
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from oarepo_model_builder.validation.utils import ImportSchema


class PublishedServiceSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(
        metadata={"doc": "Generate published service class (default)"}
    )
    config_key = ma.fields.Str(
        metadata={"doc": "Key under which actual service class is registered in config"}
    )
    proxy = ma.fields.Str(
        metadata={"doc": "name of the service proxy, will be put to _proxies_ package"}
    )
    ext_name = ma.fields.Str(
        metadata={"doc": "name under which the service is registered inside ext"},
        attribute="ext-name",
        data_key="ext-name",
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the published service class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={
            "doc": "Extra code to be put below the generated published service class"
        },
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()


class PublishedServiceConfigSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    service_id = ma.fields.String(
        attribute="service-id",
        data_key="service-id",
        metadata={"doc": "ID of the published service"},
    )
    generate = ma.fields.Bool(metadata={"doc": "Generate the service config (default)"})
    config_key = ma.fields.Str(
        metadata={
            "doc": "Key under which the actual published service config is registered in config"
        }
    )
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the published service config class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be put below the service config class"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    additional_args = ma.fields.List(
        ma.fields.String(),
        attribute="additional-args",
        data_key="additional-args",
        metadata={
            "doc": "List of additional arguments that will be passed to the published service constructor"
        },
    )
    components = ma.fields.List(
        ma.fields.String(), metadata={"doc": "List of published service components"}
    )
    skip = ma.fields.Boolean()


class PublishedServiceComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ServiceModelComponent, ExtResourceModelComponent]

    class ModelSchema(ma.Schema):
        published_service = ma.fields.Nested(
            PublishedServiceSchema,
            attribute="published-service",
            data_key="published-service",
        )
        published_service_config = ma.fields.Nested(
            PublishedServiceConfigSchema,
            attribute="published-service-config",
            data_key="published-service-config",
        )

    def process_published_service_config(self, datatype, section, **kwargs):
        if datatype.root.profile == "record":
            cfg = section.config
            cfg.setdefault("additional-args", []).append(
                f"proxied_drafts_config=self.{datatype.section_ext_resource.config['ext-service-name']}.config"
            )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        profile_module = context["profile_module"]
        module = datatype.definition["module"]["qualified"]
        module_base_upper = datatype.definition["module"]["base-upper"]
        record_prefix = datatype.definition["module"]["prefix"]

        service_package = f"{module}.services.{profile_module}.published"

        config = set_default(datatype, "published-service-config", {})

        config.setdefault(
            "config-key",
            f"{module_base_upper}_{context['profile_upper']}_PUBLISHED_SERVICE_CONFIG",
        )
        config_module = config.setdefault(
            "module",
            f"{service_package}.config",
        )
        config.setdefault(
            "class",
            f"{config_module}.{record_prefix}PublishedServiceConfig",
        )
        config.setdefault("extra-code", "")
        config.setdefault(
            "service-id",
            "published_" + datatype.definition["service-config"]["service-id"],
        )
        config.setdefault(
            "base-classes",
            [
                "oarepo_published_service.services.config.PublishedServiceConfig",
                "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin",
            ],
        )
        config.setdefault("components", [])
        # append_array(
        #     datatype,
        #     "published-service-config",
        #     "imports",
        #     {
        #         "import": "oarepo_published_service.services.config.PublishedServiceConfig",
        #         "alias": "PublishedServiceConfig",
        #     },
        # )
        # append_array(
        #     datatype,
        #     "published-service-config",
        #     "imports",
        #     {"import": "oarepo_runtime.services.config.service.PermissionsPresetsConfigMixin"},
        # )
        convert_config_to_qualified_name(config)

        service = set_default(datatype, "published-service", {})

        service.setdefault("generate", True)
        config.setdefault("generate", service["generate"])

        service.setdefault(
            "config-key",
            f"{module_base_upper}_{context['profile_upper']}_PUBLISHED_SERVICE_CLASS",
        )
        service.setdefault("proxy", "current_published_service")
        service_module = service.setdefault("module", f"{service_package}.service")
        service.setdefault("class", f"{service_module}.{record_prefix}PublishedService")
        service.setdefault("extra-code", "")
        service.setdefault(
            "base-classes",
            ["oarepo_published_service.services.service.PublishedService"],
        )
        service.setdefault(
            "imports",
            [
                # {
                #     "import": "oarepo_published_service.services.service.PublishedService",
                #     "alias": "PublishedService",
                # }
            ],
        )
        convert_config_to_qualified_name(service)

    def process_published_service(self, datatype, section, **kwargs):
        cfg = section.config
        cfg.setdefault(
            "ext-name",
            "published_" + datatype.section_ext_resource.config["ext-service-name"],
        )
