import bpkio_api.models as models
import click
import cloup

import bpkio_cli.click_options as bic_options
from bpkio_cli.commands.creators.sources import create
from bpkio_cli.commands.misc.compatibility_check import check_compatibility
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.core.app_context import AppContext


def get_sources_commands():
    root_endpoint = "sources"
    root: cloup.Group = create_resource_group(
        "source",
        resource_type=models.SourceIn,
        endpoint_path=[root_endpoint],
        aliases=["src", "sources"],
        with_content_commands=["all"],
        traversal_commands=[usage],
        default_fields=["id", "name", "type", "format", "url"],
        extra_commands=[create, check_compatibility],
    )

    return [
        root,
        create_resource_group(
            "asset",
            resource_type=models.AssetSource,
            endpoint_path=[root_endpoint, "asset"],
            aliases=["assets"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=[
                "info",
                "url",
                "check",
                "table",
                "read",
                "play",
                "profile",
                "download",
            ],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        create_resource_group(
            "live",
            resource_type=models.LiveSource,
            endpoint_path=[root_endpoint, "live"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["all"],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        create_resource_group(
            "asset-catalog",
            resource_type=models.AssetCatalogSource,
            endpoint_path=[root_endpoint, "asset_catalog"],
            aliases=["catalog", "catalogs"],
            default_fields=["id", "name", "url"],
            with_content_commands=[
                "info",
                "url",
                "check",
                "table",
                "read",
                "play",
                "profile",
                "download",
            ],
            traversal_commands=[usage],
            extra_commands=[check_compatibility],
        ),
        create_resource_group(
            "ad-server",
            resource_type=models.AdServerSource,
            endpoint_path=[root_endpoint, "ad_server"],
            aliases=["ads"],
            with_content_commands=["info", "url", "check", "table", "read"],
            default_fields=["id", "name", "url"],
            traversal_commands=[usage],
        ),
        create_resource_group(
            "slate",
            resource_type=models.SlateSource,
            endpoint_path=[root_endpoint, "slate"],
            aliases=["slates"],
            default_fields=["id", "name", "format", "url"],
            with_content_commands=["url", "check", "play"],
            traversal_commands=[usage],
        ),
        create_resource_group(
            "origin",
            resource_type=models.OriginSource,
            endpoint_path=[root_endpoint, "origin"],
            aliases=["origins"],
            default_fields=["id", "name", "url"]
        ),
    ]


# COMMAND: USAGE
@cloup.command(help="Find all Services that use the source")
@bic_options.list(default_fields=["id", "name", "type"])
@bic_options.output_formats
@click.pass_obj
def usage(
    obj: AppContext,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
    **kwargs
):
    select_fields = list(select_fields)
    id = obj.current_resource.id
    source = obj.api.sources.retrieve(id)

    services = obj.api.services.list()

    selected_services = []
    for service in services:
        svc = obj.api.services.retrieve(service.id)

        if hasattr(svc, "source") and getattr(svc.source, "id") == id:
            selected_services.append(svc)
            select_fields.append("source")

        if hasattr(svc, "replacement") and getattr(svc.replacement, "id") == id:
            selected_services.append(svc)
            select_fields.append("replacement")

        if isinstance(source, models.LiveSource):
            if isinstance(svc, models.VirtualChannelService):
                if svc.baseLive.id == id:
                    selected_services.append(svc)
                    select_fields.append("baseLive")

        if isinstance(source, models.AdServerSource):
            if isinstance(svc, models.AdInsertionService):
                if svc.vodAdInsertion and svc.vodAdInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("vodAdInsertion.adServer.id")
                if svc.liveAdPreRoll and svc.liveAdPreRoll.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdPreRoll.adServer.id")
                if svc.liveAdReplacement and svc.liveAdReplacement.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.adServer.id")

            if isinstance(svc, models.VirtualChannelService):
                if svc.adBreakInsertion and svc.adBreakInsertion.adServer.id == id:
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.adServer.id")

        if isinstance(source, models.SlateSource):
            if isinstance(svc, models.AdInsertionService):
                if (
                    svc.liveAdReplacement
                    and svc.liveAdReplacement.gapFiller
                    and svc.liveAdReplacement.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("liveAdReplacement.gapFiller.id")

            if isinstance(svc, models.VirtualChannelService):
                if (
                    svc.adBreakInsertion
                    and svc.adBreakInsertion.gapFiller
                    and svc.adBreakInsertion.gapFiller.id == id
                ):
                    selected_services.append(svc)
                    select_fields.append("adBreakInsertion.gapFiller.id")

    if len(selected_services):
        obj.response_handler.treat_list_resources(
            selected_services,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            id_only=id_only,
            return_first=return_first,
        )
    else:
        click.secho("No services found that use this source")
