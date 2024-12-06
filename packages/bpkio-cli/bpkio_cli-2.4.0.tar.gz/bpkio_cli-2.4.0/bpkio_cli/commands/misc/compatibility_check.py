import click
import cloup
from bpkio_api.exceptions import BroadpeakIoHelperError
from bpkio_api.models.Sources import (AssetCatalogSourceIn, AssetSourceIn,
                                      LiveSourceIn, SourceIn)
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.utils.url_builders import get_source_handler
from bpkio_cli.writers.colorizer import Colorizer as CL
from media_muncher.analysers.hls_compare import HlsProfileComparer
from media_muncher.handlers import factory
from media_muncher.handlers.hls import HLSHandler
from pydantic import HttpUrl


@cloup.command(
    name="check-compatibility",
    aliases=["comp"],
    help="Validate compatibility of a resource or stream with a particular HLS source",
)
@cloup.option_group(
    "Target stream to validate against",
    cloup.option(
        "--source",
        "source_id",
        help="ID of a source to validate against",
        required=False,
    ),
    cloup.option(
        "--url",
        help="URL of a stream to validate against",
        required=False,
    ),
    constraint=cloup.constraints.mutually_exclusive,
)
@click.pass_obj
def check_compatibility(obj: AppContext, source_id: str, url: str):

    click.secho("Limitations:", fg="yellow")
    click.secho(
        "- This feature only offers a lightweight compatibility check, and does not validate all rules used by the manifest manipulator. \n"
        "- It currently only covers video variant streams"
        "A positive or negative compatibility statement is therefore no guarantee of the same behaviour being observed in a configured system.",
        fg="yellow",
    )
    click.secho("")

    candidate_resource = obj.current_resource
    if isinstance(candidate_resource, HttpUrl):
        candidate_handler = factory.create_handler(
            candidate_resource,
        )
    else:
        candidate_handler = get_source_handler(candidate_resource)
    if not isinstance(candidate_handler, HLSHandler):
        raise BroadpeakIoHelperError(
            "You can only check compatibility of HLS resources"
        )

    # If no source_id, we get it from the context
    if not source_id and not url:
        source_id = obj.cache.last_id_by_type(SourceIn)

    if source_id:
        source_resource = obj.api.sources.retrieve(source_id)
        if not isinstance(
            source_resource, (AssetSourceIn, LiveSourceIn, AssetCatalogSourceIn)
        ):
            raise BroadpeakIoHelperError(
                f"You cannot compare against a source of type {source_resource.__class__.__name__}"
            )

        target_handler = get_source_handler(source_resource)
        target_description = source_resource.summary
    elif url:
        target_handler = factory.create_handler(url)
        target_description = url
    else:
        click.secho(
            "No source specified and none usable in the cache, aborting", fg="red"
        )
        return

    if not isinstance(target_handler, HLSHandler):
        raise BroadpeakIoHelperError(
            "You can only check compatibility with HLS sources"
        )

    comparer = HlsProfileComparer()
    comparer.set_target(target_handler)
    result = comparer.check_candidate(candidate_handler)

    # Analyse results
    if result["is_compatible"] is False:
        click.secho(
            f"NO, this resource or stream seems not to be compatible with target {target_description}",
            fg="red",
        )
    else:
        click.secho(
            f"YES, this resource or stream seems to be compatible with target {target_description}",
            fg="green",
        )

    # Show a summary
    click.secho("\nFor the following renditions in the source:")
    for rend in result["renditions"]:
        src = rend["source"]
        click.secho(
            f" - source rendition: \"{CL.high2(src.uri)}\" with codec string '{src.stream_info.codecs}'"
        )

        if len(rend["candidates"]) == 0:
            click.secho("   no match was found", fg="red")
        else:
            for cand in rend["candidates"]:
                click.secho("   a match was found: ", fg="green", nl=False)
                click.secho(f'"{CL.high2(cand.uri)}"')

    if len(result["additional_renditions"]) > 0:
        click.secho("\nAdditional unnecessary renditions were found in the resource:")
        for rend in result["additional_renditions"]:
            click.secho(
                f" - {CL.high2(rend.uri)} with codec string '{rend.stream_info.codecs}'"
            )
