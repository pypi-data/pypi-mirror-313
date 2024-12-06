import re
from collections import OrderedDict
from typing import List
from urllib.parse import urlparse, urlunparse

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.exceptions import ResourceExistsError
from bpkio_api.helpers.source_type import SourceTypeDetector
from bpkio_api.models import (
    AdServerQueryParameter,
    AdServerQueryParameterType,
    AdServerSourceIn,
    AssetCatalogSourceIn,
    AssetSourceIn,
    LiveSourceIn,
    SlateSourceIn,
    SourceType,
)
from bpkio_api.models.Sources import ADSERVER_SYSTEM_VALUES, OriginConfig
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.writers.colorizer import Colorizer as CL
from InquirerPy.base.control import Choice


@bic_res_cmd.command(
    takes_id_arg=False,
    help="Create a Source from just a URL. "
    "The CLI will work out what type of Source it is and create it accordingly",
)
@cloup.argument("url", help="URL of the source", required=False)
@cloup.option("--name", help="Name for the source", required=False)
@cloup.option(
    "-h",
    "--header",
    "headers",
    type=str,
    multiple=True,
    help="Headers needed to access the source. Must be in the format `key=value` or `key: value`. "
    + "The key should be in the exact format expected in the header. "
    + "To pass multiple params, repeat the option, eg. -h key1=value1 -h key2=value2",
)
@cloup.option(
    "--assist/--no-assist", help="Assist with the creation of the source", default=True
)
@click.pass_obj
def create(
    obj: AppContext,
    url: str,
    name: str,
    assist: bool,
    headers: List[str],
):
    metadata_cache = obj.cache

    if not url:
        url = prompt.text(
            message="URL of the source",
            validate=lambda url: re.match(r"^https?://", url.strip()),
            invalid_message=("Your URL must be a valid HTTP URL"),
        )

    source_type = SourceTypeDetector.determine_source_type(url, headers=headers)
    if not source_type:
        raise Exception("Could not determine the type of source for that URL")

    click.secho("This appears to be a source of type: %s" % source_type.value)

    if source_type == SourceType.ASSET:
        source_type = prompt.select(
            message="From this, create",
            choices=[
                Choice(SourceType.ASSET, name="Asset"),
                Choice(SourceType.ASSET_CATALOG, name="Asset Catalog"),
            ],
            multiselect=False,
        )

    if source_type == SourceType.ASSET_CATALOG:
        url_parts = urlparse(url)
        path_parts = url_parts.path.split("/")[1:-1]
        paths = ["/"]
        last_path = ""
        for p in path_parts:
            last_path = last_path + "/" + p
            paths.append(last_path + "/")

        common_path = prompt.select(
            message="Common path for all assets",
            choices=paths,
            multiselect=False,
        )

        new_url = url_parts._replace(path=common_path, query="")
        new_url = urlunparse(new_url)

        sample = url.replace(new_url, "")

    if not name:
        name = prompt.text(message="Name for the source")

    origin = OriginConfig(customHeaders=[])
    for header_str in headers:
        try:
            key, value = header_str.split("=", 1)
        except ValueError:
            key, value = header_str.split(":", 1)
        origin.customHeaders.append(dict(name=key, value=value.strip()))

    try:
        match source_type:
            case SourceType.LIVE:
                source = obj.api.sources.live.create(
                    LiveSourceIn(name=name, url=url, origin=origin)
                )
            case SourceType.AD_SERVER:
                (url, queryParams, metadata) = treat_adserver_url(url, assist=assist)
                source = obj.api.sources.ad_server.create(
                    AdServerSourceIn(
                        name=name, url=url, queryParameters=queryParams, adOrigin=origin
                    )
                )
                for k, v in metadata.items():
                    metadata_cache.record_metadata(source, k, v)

            case SourceType.SLATE:
                source = obj.api.sources.slate.create(SlateSourceIn(name=name, url=url))
            case SourceType.ASSET:
                source = obj.api.sources.asset.create(
                    AssetSourceIn(name=name, url=url, origin=origin)
                )
            case SourceType.ASSET_CATALOG:
                source = obj.api.sources.asset_catalog.create(
                    AssetCatalogSourceIn(
                        name=name, url=new_url, assetSample=sample, origin=origin
                    )
                )
            case _:
                raise BroadpeakIoCliError("Unrecognised source type '%s'" % source_type)

        obj.response_handler.treat_single_resource(source)

    except ResourceExistsError:
        click.echo(CL.error("A source with this URL already exists"))
        other_sources = obj.api.sources.search(value=url)

        click.echo(f"There are {len(other_sources)} other sources with this URL: ")
        for s in other_sources:
            obj.response_handler.treat_single_resource(s)


def treat_adserver_url(url, assist: bool = True):
    metadata_to_save = {}

    parts = url.split("?")

    if len(parts) == 1:
        parts.append("")

    queries = parts[1]
    updated_queries = []

    choices = dict(
        custom="CUSTOM: a static value (or a value with $* variables)",
        arg="QUERY PARAM: pass-through from a query parameter on service URL (as $arg_*)",
        header="HEADER: pass-through from a header on service URL (as $http_*)",
        variable="VARIABLE: pass-through of a system variable",
        keep="Keep unchanged (same as CUSTOM)",
        remove="Remove this parameter",
    )

    if len(queries) and assist:
        for p in queries.split("&"):
            (k, val) = p.split("=")
            original_val = val
            qp_type = AdServerQueryParameterType.custom

            # Suggest replacement for query parameters

            default = "custom"
            if val.startswith("$"):
                default = "variable"
            if val.startswith("$arg_"):
                default = "arg"
            if val.startswith("$http_"):
                default = "header"
            if val.startswith("[") or val.startswith("{"):
                default = "arg"

            # Reorder the choices accordingly
            reordered_choices = reorder_dict(choices, default)

            treatment = prompt.fuzzy(
                message=f"Parameter '{k}' (current value '{val}')",
                choices=[Choice(k, name=v) for k, v in reordered_choices.items()],
            )

            if treatment == "keep":
                val = val

            if treatment == "custom":
                val = prompt.text(message="Value", default=val, level=1)

            if treatment == "arg":
                qp_type = AdServerQueryParameterType.from_query_parameter
                if val.startswith("$arg_"):
                    val = val.replace("$arg_", "")
                else:
                    val = k

                val = prompt.text(
                    message="Name of the query param on the incoming request",
                    default=val,
                    level=1,
                )

                metadata_to_save[val] = original_val

            if treatment == "header":
                qp_type = AdServerQueryParameterType.from_header
                val = prompt.fuzzy(
                    message="Header on the incoming request",
                    choices=["User-Agent", "Host", "X-Forwarded-For", "(other)"],
                    level=1,
                )

                if val == "(other)":
                    val = prompt.text(
                        message="Name of the header on the incoming request",
                        level=1,
                    )

            if treatment == "variable":
                qp_type = AdServerQueryParameterType.from_variable
                val = prompt.fuzzy(
                    message="System value",
                    choices=[
                        Choice(s[0], name=f"{s[2]}: {s[1]}   (internally: {s[0]})")
                        for s in ADSERVER_SYSTEM_VALUES
                    ],
                    level=1,
                )

            if treatment == "remove":
                continue

            updated_queries.append(
                AdServerQueryParameter(name=k, type=qp_type, value=val)
            )

    return (parts[0], updated_queries, metadata_to_save)


def make_dynamic_param(name, mode):
    if mode == "header":
        return f"$http_{name.lower().replace('-','_')}"
    if mode == "param":
        return f"$arg_{name.lower().replace('-','_')}"


# Function to reorder dictionary
def reorder_dict(d, first_key):
    new_dict = OrderedDict()
    if first_key in d:
        new_dict[first_key] = d[first_key]
    for k, v in d.items():
        if k != first_key:
            new_dict[k] = v
    return new_dict
