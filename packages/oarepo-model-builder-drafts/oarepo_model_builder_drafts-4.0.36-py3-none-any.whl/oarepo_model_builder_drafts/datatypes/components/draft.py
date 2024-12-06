import marshmallow as ma
from oarepo_model_builder.datatypes import (
    DataType,
    DataTypeComponent,
    ModelDataType,
    Section,
)
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.model import Link
from oarepo_model_builder.utils.links import url_prefix2link
from oarepo_model_builder.utils.python_name import Import


def get_draft_schema():
    from ..draft import DraftDataType

    return DraftDataType.validator()


def remove_links_by_names(links_section, link_names_to_remove):
    links_to_remove = []
    for link in links_section:
        if link.name in link_names_to_remove:
            links_to_remove.append(link)
    for link in links_to_remove:
        links_section.remove(link)


class DraftComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        draft = ma.fields.Nested(get_draft_schema)

    def process_links(self, datatype, section: Section, **kwargs):
        url_prefix = url_prefix2link(datatype.definition["resource-config"]["base-url"])
        html_url_prefix = url_prefix2link(
            datatype.definition["resource-config"]["base-html-url"]
        )

        if datatype.root.profile == "record":
            remove_links_by_names(section.config["links_item"], {"self", "self_html"})
            remove_links_by_names(
                section.config["links_search_item"], {"self", "self_html"}
            )

            section.config["links_search_drafts"] = [
                Link(
                    name=None,
                    link_class="pagination_links",
                    link_args=[f'"{{+api}}/user{url_prefix}{{?args*}}"'],
                    imports=[
                        Import("invenio_records_resources.services.pagination_links")
                    ],
                ),
                Link(
                    name=None,
                    link_class="pagination_links_html",
                    link_args=[f'"{{+ui}}/user{url_prefix}{{?args*}}"'],
                    imports=[
                        Import("oarepo_runtime.services.records.pagination_links_html")
                    ],
                ),
            ]

            section.config["links_search_versions"] = [
                Link(
                    name=None,
                    link_class="pagination_links",
                    link_args=[f'"{{+api}}{url_prefix}{{id}}/versions{{?args*}}"'],
                    imports=[
                        Import("invenio_records_resources.services.pagination_links")
                    ],
                ),
            ]

            section.config["links_item"] += [
                Link(
                    name="self",
                    link_class="ConditionalLink",
                    link_args=[
                        "cond=is_published_record()",
                        f'if_=RecordLink("{{+api}}{url_prefix}{{id}}"',
                        'when=has_permission("read"))',
                        f'else_=RecordLink("{{+api}}{url_prefix}{{id}}/draft"',
                        'when=has_permission("read_draft"))',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.ConditionalLink"),
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.is_published_record"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="self_html",
                    link_class="ConditionalLink",
                    link_args=[
                        "cond=is_published_record()",
                        f'if_=RecordLink("{{+ui}}{html_url_prefix}{{id}}"',
                        'when=has_permission("read"))',
                        f'else_=RecordLink("{{+ui}}{html_url_prefix}{{id}}/preview"',
                        'when=has_permission("read_draft"))',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.ConditionalLink"),
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.is_published_record"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="edit_html",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+ui}}{html_url_prefix}{{id}}/edit"',
                        'when=has_draft() & has_permission("read_draft")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_draft"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="latest",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}/versions/latest"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="latest_html",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+ui}}{html_url_prefix}{{id}}/latest"',
                        'when=has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="draft",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}/draft"',
                        'when=has_draft() & has_permission("read_draft")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="record",  # this links to self or record with the same id as draft for drafts; but perhaps discuss whether this is optimal
                    # desired behavioral; ie. it could also link last version if the record isn't available
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}"',
                        'when=has_published_record() & has_permission("read")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                        Import("oarepo_runtime.services.config.has_published_record"),
                    ],
                ),
                Link(
                    name="publish",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}/draft/actions/publish"',
                        'when=has_permission("publish")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="versions",
                    link_class="RecordLink",
                    link_args=[
                        f'"{{+api}}{url_prefix}{{id}}/versions"',
                        'when=has_permission("search_versions")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
            ]

            section.config["links_search_item"] += [
                Link(
                    name="self",
                    link_class="ConditionalLink",
                    link_args=[
                        "cond=is_published_record()",
                        f'if_=RecordLink("{{+api}}{url_prefix}{{id}}"',
                        'when=has_permission("read"))',
                        f'else_=RecordLink("{{+api}}{url_prefix}{{id}}/draft"',
                        'when=has_permission("read_draft"))',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.ConditionalLink"),
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.is_published_record"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
                Link(
                    name="self_html",
                    link_class="ConditionalLink",
                    link_args=[
                        "cond=is_published_record()",
                        f'if_=RecordLink("{{+ui}}{html_url_prefix}{{id}}"',
                        'when=has_permission("read"))',
                        f'else_=RecordLink("{{+ui}}{html_url_prefix}{{id}}/preview"',
                        'when=has_permission("read_draft"))',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.ConditionalLink"),
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.services.config.is_published_record"),
                        Import("oarepo_runtime.services.config.has_permission"),
                    ],
                ),
            ]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "draft":
            published_record_datatype: DataType = context["published_record"]
            datatype.published_record = published_record_datatype

            properties = set_default(datatype, "properties", {})
            for property_key, property_value in published_record_datatype.definition[
                "properties"
            ].items():  # this should
                properties.setdefault(property_key, property_value)
