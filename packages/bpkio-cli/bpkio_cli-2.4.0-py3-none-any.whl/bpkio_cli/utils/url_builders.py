from typing import List, Optional
from urllib.parse import parse_qs, urljoin, urlparse, urlunparse

import bpkio_cli.utils.prompt as prompt
import click
from bpkio_api.models import (AdInsertionService, AdServerSourceIn,
                              AssetCatalogSourceIn, BaseResource, SourceIn,
                              SourceType, VirtualChannelService)
from bpkio_api.models.Services import ContentReplacementService
from bpkio_api.models.Sources import ADSERVER_SYSTEM_VALUES
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.utils.urls import (add_query_parameters_from_dict,
                                  add_query_parameters_from_list,
                                  validate_ipv4_or_domain)
from bpkio_cli.writers.colorizer import Colorizer
from media_muncher.handlers import ContentHandler, factory

NEW = "-- add new --"
DELETED = "__DELETED__"
UNSET = "__UNSET__"


def get_source_handler(
    source: SourceIn,
    extra_url: Optional[str] = None,
    additional_query_params: Optional[List[str]] = None,
    additional_headers: Optional[List[str]] = None,
    subplaylist_index: Optional[int] = None,
    user_agent: Optional[str] = None,
) -> ContentHandler:
    if isinstance(source, AssetCatalogSourceIn):
        # Ask for extra portion of URL if it wasn't supplied
        if not extra_url:
            extra_url = ask_for_asset_catalog_sub_path(source)

    url_to_read = source.make_full_url(extra_url)

    if user_agent == "SELECT":
        user_agent = ask_for_user_agent(source)
    else:
        user_agent = CONFIG.get_user_agent()

    if isinstance(source, AdServerSourceIn):
        # Fill query parameters
        if not extra_url or "?" not in url_to_read:
            filled_params = ask_for_adserver_query_params(source, user_agent=user_agent)
            url_to_read = add_query_parameters_from_dict(url_to_read, filled_params)

    # Additional query parameters
    if additional_query_params:
        url_to_read = add_query_parameters_from_list(
            url_to_read, additional_query_params
        )

    handler: ContentHandler = factory.create_handler(
        url_to_read,
        user_agent=CONFIG.get_user_agent(user_agent),
        explicit_headers=additional_headers,
    )
    if subplaylist_index:
        if handler.has_children():
            handler = handler.get_child(subplaylist_index)
        else:
            click.secho(
                "`--sub` cannot be used with this source, as it has no children URLs. Using main URL instead",
                fg="red",
            )

    return handler


def get_service_handler(
    service,
    api,
    replacement_fqdn: Optional[str],
    extra_url: Optional[str],
    additional_query_params: Optional[List[str]],
    additional_headers: Optional[List[str]],
    subplaylist_index: Optional[int],
    user_agent: Optional[str],
    service_as_param: Optional[bool] = False
) -> ContentHandler:
    """Calculates the URL to call for a Service, based on its type and Source"""
    if not subplaylist_index and service_as_param:
        url_to_read = service.make_full_url(service_as_param=service_as_param)
    else:
        url_to_read = service.make_full_url()
        
    if isinstance(service, AdInsertionService):
        source_type = service.source.type
        source_id = service.source.id

        if source_type == SourceType.ASSET_CATALOG:
            # Ask for extra portion of URL if it wasn't supplied
            if not extra_url:
                source = api.sources.asset_catalog.retrieve(source_id)
                extra_url = ask_for_asset_catalog_sub_path(source)

            url_to_read = urljoin(service.url, extra_url)

    # replace the fqdn if necessary
    if replacement_fqdn:
        if replacement_fqdn == "SELECT":
            replacement_fqdn = ask_for_fqdn(service)

        parsed_url = urlparse(url_to_read)

        # replacement FQDN could contain protocol scheme
        prefix_parts = replacement_fqdn.split("://")
        if len(prefix_parts) == 1:
            url_to_read = urlunparse(parsed_url._replace(netloc=prefix_parts[0]))
        else:
            url_to_read = urlunparse(
                parsed_url._replace(scheme=prefix_parts[0], netloc=prefix_parts[1])
            )

    # In case it's a service with ad insertion, and the ad server has query params,
    # prompt for values for the ones expected to be passed through
    ad_config = None
    if isinstance(service, AdInsertionService):
        ad_config = get_first_matching_key_value(
            service, ["vodAdInsertion", "liveAdPreRoll", "liveAdReplacement"]
        )
    if isinstance(service, VirtualChannelService):
        if service.adBreakInsertion:
            ad_config = service.adBreakInsertion

    if ad_config and ad_config.adServer:
        queries = {}
        if extra_url and "?" in extra_url:
            query_string = extra_url.split("?")[1]
            queries = {k: v for k, v in (x.split("=") for x in query_string.split("&"))}

        filled_params = ask_for_adserver_query_params(
            ad_config.adServer,
            existing_params=queries,
            for_service=True,
            user_agent=user_agent,
        )
        url_to_read = add_query_parameters_from_dict(url_to_read, filled_params)

    if user_agent == "SELECT":
        user_agent = ask_for_user_agent(service)

    # Additional query parameters
    query_params_to_add = []
    additional_query_params_split = {}

    # split the ones passed explicitely
    if additional_query_params:
        additional_query_params_split = {
            item.split("=")[0]: item.split("=")[1]
            for item in "&".join(additional_query_params).split("&")
        }

    # We need to first check whether there are any expected to be forwarded to the origin
    if (
        service.advancedOptions
        and service.advancedOptions.queryManagement
        and service.advancedOptions.queryManagement.forwardInOriginRequest
    ):
        params_to_forward = (
            service.advancedOptions.queryManagement.forwardInOriginRequest
        )
        # retrieve their value from the source
        if isinstance(service, AdInsertionService):
            source_url = service.source.url
        elif isinstance(service, (VirtualChannelService, ContentReplacementService)):
            source_url = service.baseLive.url

        # parse the URL to extract the parameters
        source_url_params = parse_qs(urlparse(source_url).query)

        # Now we ensure that they are all filled
        for param in params_to_forward:
            if param in source_url_params:
                source_val = source_url_params[param][0]

                if param in additional_query_params_split:
                    # extract value and remove it from that array
                    val = additional_query_params_split.pop(param)

                    # raise a warning if different
                    if val != source_val:
                        click.secho(
                            Colorizer.log(
                                text=f'Parameter `{param}` with value "{val}" has a different value "{source_val}" in the source. This may cause issues!',
                                type="warning",
                            )
                        )
                    query_params_to_add.append(f"{param}={val}")

                else:
                    # raise a warning if not present
                    if param in source_url_params:
                        click.secho(
                            Colorizer.log(
                                f'Parameter `{param}` from the source needs forwarding. I added it with value "{source_val}"!',
                                type="warning",
                            )
                        )
                    query_params_to_add.append(f"{param}={source_url_params[param][0]}")

    # Then we add any one left
    for param in additional_query_params_split:
        query_params_to_add.append(f"{param}={additional_query_params_split[param]}")

    if query_params_to_add:
        url_to_read = add_query_parameters_from_list(url_to_read, query_params_to_add)

    handler: ContentHandler = factory.create_handler(
        url_to_read,
        from_url_only=True,
        user_agent=CONFIG.get_user_agent(user_agent),
        explicit_headers=additional_headers,
    )
    if subplaylist_index:
        if handler.has_children():
            additional_child_query_params = {}
            if service_as_param:
                additional_child_query_params["bpkio_serviceid"] = service.hash
            handler = handler.get_child(subplaylist_index, additional_query_params=additional_child_query_params)
        else:
            click.secho(
                "`--sub` cannot be used with this source, as it has no children URLs. Using main URL instead",
                fg="red",
            )

    return handler


def get_first_matching_key_value(resource: BaseResource, possible_keys: List[str]):
    for key in possible_keys:
        if getattr(resource, key):
            return getattr(resource, key)
    return None


def ask_for_adserver_query_params(
    adserver: AdServerSourceIn, existing_params={}, for_service=False, user_agent=""
):
    obj: AppContext = click.get_current_context().obj

    section_title_shown = False

    metadata_cache = obj.cache
    filled_params = dict()

    for qp in adserver.queryParameters:
        if not qp.value:
            # Workaround for issue with incorrect conversion of empty `queries` when platform moved to `queryParameters`
            continue

        input_param = (
            None  # the name of the parameter that will be displayed at the prompt
        )
        param_to_fill = (
            None  # the name of the parameter that will be filled in the final URL
        )

        if qp.is_from_query_parameter():
            input_param = qp.value.replace("$arg_", "")  # replace in case it's a custom qp
            # determine output param name
            if for_service:
                if input_param in [
                    "serviceid",
                    "sessionid",
                    "bpkio_sessionid",
                    "bpkio_serviceid",
                ]:
                    continue
                else:
                    param_to_fill = input_param
            else:
                param_to_fill = qp.name
                
        elif qp.is_from_header():
            if qp.value.lower().replace("-", "_").replace("$http_", "") == "user_agent":
                input_param = qp.value
                param_to_fill = qp.name
                metadata_cache.record_metadata(adserver, input_param, user_agent)

        elif qp.is_from_variable():
            if not for_service:
                # Check if they are system values (which cannot be filled in the case of a source)
                for system_value in ADSERVER_SYSTEM_VALUES:
                    if qp.value == system_value[0]:
                        input_param = qp.value
                        param_to_fill = qp.name

        if not input_param:
            continue

        # Now start replacing
        cached_values = metadata_cache.get_metadata(adserver, input_param)

        if qp.name in existing_params:
            cached_values.insert(0, existing_params[qp.name])

        input_val = UNSET

        if obj.config.get("use_prompts"):
            if not section_title_shown:
                click.secho("\nQuery params to pass to the ad server", fg="white")
                section_title_shown = True

            while input_val in [DELETED, UNSET]:
                if cached_values:

                    def _handle_delete(selected_value):
                        metadata_cache.remove_metadata(
                            adserver, input_param, selected_value
                        )
                        return DELETED

                    input_val = prompt.select(
                        message=f"Parameter '{input_param}'",
                        choices=cached_values + [NEW],
                        multiselect=False,
                        default=cached_values[0],
                        keybinding_delete=_handle_delete,
                        keybinding_skip_all_prompts=True,
                    )

                if not cached_values:
                    input_val = prompt.text(message=f"Parameter '{input_param}'")

                if input_val == NEW:
                    input_val = prompt.text(message="New value: ", level=1)

        else:
            if cached_values:
                input_val = cached_values[0]
            else:
                input_val = ""

            click.secho(f"> Parameter '{input_param}': ", fg="white", nl=False)
            click.secho(input_val, fg="blue", bold=True)

        filled_params[param_to_fill] = input_val

        if input_val is not None and input_val != "":
            metadata_cache.record_metadata(adserver, input_param, input_val)
    return filled_params


def ask_for_asset_catalog_sub_path(source: AssetCatalogSourceIn):
    extra_url = source.assetSample

    obj = click.get_current_context().obj

    metadata_cache = obj.cache
    cached_values = metadata_cache.get_metadata(source, "subPath")

    extra_url = UNSET

    if obj.config.get("use_prompts"):
        while extra_url in [UNSET, DELETED]:
            click.echo()
            if cached_values:

                def _handle_delete(selected_value):
                    metadata_cache.remove_metadata(source, "subPath", selected_value)
                    return DELETED

                extra_url = prompt.select(
                    message="Sub-path",
                    choices=cached_values + [NEW],
                    multiselect=False,
                    default=cached_values[0],
                    keybinding_delete=_handle_delete,
                    keybinding_skip_all_prompts=True,
                )

            if not cached_values or extra_url == NEW:
                extra_url = prompt.text(
                    message="Sub-path",
                    long_instruction="Defaults to the Asset Catalog asset sample",
                    default=source.assetSample,
                )

    else:
        if cached_values:
            extra_url = cached_values[0]
        else:
            extra_url = source.assetSample

        click.secho("> Sub-path: ", fg="white", nl=False)
        click.secho(extra_url, fg="bright_blue", bold=True)

    metadata_cache.record_metadata(source, "subPath", extra_url)

    return extra_url


def ask_for_fqdn(service):
    fqdn = None
    obj: AppContext = click.get_current_context().obj
    metadata_cache = obj.cache
    cached_fqdns = metadata_cache.get_metadata(service, "fqdn")

    fqdn = UNSET

    if obj.config.get("use_prompts"):
        while fqdn in [UNSET, DELETED]:
            if cached_fqdns:

                def _handle_delete(selected_value):
                    metadata_cache.remove_metadata(service, "fqdn", selected_value)
                    return DELETED

                fqdn = prompt.select(
                    message="Domain name (for CDN)",
                    choices=cached_fqdns + [NEW],
                    multiselect=False,
                    default=cached_fqdns[0],
                    keybinding_delete=_handle_delete,
                    keybinding_skip_all_prompts=True,
                )

            if not cached_fqdns or fqdn == NEW:
                fqdn = prompt.text(
                    message="Domain name (for CDN)",
                    default="",
                    validate=lambda x: validate_ipv4_or_domain(x),
                    invalid_message="Must be a well-formed domain name or IP address",
                    keybinding_skip_all_prompts=True,
                )

    else:
        if cached_fqdns:
            fqdn = cached_fqdns[0]
        else:
            fqdn = "CUSTOM_FQDN"

        click.secho("> FQDN: ", fg="white", nl=False)
        click.secho(fqdn, fg="blue", bold=True)

    metadata_cache.record_metadata(service, "fqdn", fqdn)

    return fqdn


def ask_for_user_agent(resource):
    ua = UNSET
    obj: AppContext = click.get_current_context().obj
    metadata_cache = obj.cache
    cached_useragents = metadata_cache.get_metadata(resource, "user_agent")

    if obj.config.get("use_prompts"):
        click.echo()
        while ua in [UNSET, DELETED]:
            if cached_useragents:

                def _handle_delete(selected_value):
                    metadata_cache.remove_metadata(
                        resource, "user_agent", selected_value
                    )
                    return DELETED

                ua = prompt.select(
                    message="User agent to use: ",
                    choices=cached_useragents + [NEW],
                    multiselect=False,
                    default=cached_useragents[0],
                    keybinding_delete=_handle_delete,
                    keybinding_skip_all_prompts=True,
                )

            if not cached_useragents or ua == NEW:
                ua = prompt.text(
                    message="User agent (label or full string)",
                    default="",
                )

    else:
        if cached_useragents:
            ua = cached_useragents[0]
        else:
            ua = None

        click.secho("> User-Agent: ", fg="white", nl=False)
        click.secho(ua, fg="blue", bold=True)

    metadata_cache.record_metadata(resource, "user_agent", ua)

    return ua
