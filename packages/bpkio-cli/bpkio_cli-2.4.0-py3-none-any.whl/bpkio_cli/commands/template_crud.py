import builtins
import datetime
import re
import time
from typing import Callable, List, Optional

import bpkio_api.mappings as mappings
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder
from bpkio_api.helpers.update import edit_property
from bpkio_api.models import MediaFormat
from bpkio_api.models.Services import ServiceIn
from bpkio_api.models.Sources import SourceIn
from media_muncher.handlers.dash import DASHHandler
from media_muncher.handlers.hls import HLSHandler
from pydantic import HttpUrl, parse_obj_as
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
from bpkio_cli.commands.package import package_resources
from bpkio_cli.commands.source_check import display_source_status
from bpkio_cli.core.api_resource_helpers import (
    get_api_endpoint,
    get_content_handler,
    retrieve_api_resource_from_chain,
)
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.response_handler import save_json, save_resource
from bpkio_cli.monitor.live_monitor import monitor_hls
from bpkio_cli.utils import prompt
from bpkio_cli.utils.editor import edit_payload
from bpkio_cli.utils.profile_maker import make_transcoding_profile
from bpkio_cli.writers.breadcrumbs import (
    display_bpkio_session_info,
    display_resource_info,
    display_tip,
)
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.content_display import display_content
from bpkio_cli.writers.players import StreamPlayer
from bpkio_cli.writers.urls import pretty_url

console = Console(stderr=True)


def create_resource_group(
    name: str,
    resource_type: type,
    endpoint_path: List[str],
    title: str | None = None,
    aliases: List[str] = [],
    default_fields=["id", "name", "type"],
    with_content_commands: List[str] = [],
    traversal_commands: List[cloup.Command | Callable] = [],
    extra_commands: List[cloup.Command | Callable] = [],
):
    """Generates a group of CLI commands for CRUD-based resources

    Args:
        name (str): The name of the command group
        aliases (List[str], optional): Aliases for the command name. Defaults to none.
        default_fields (list, optional): Base resource fields used for table displays.
            Defaults to ["id", "name", "type"].
        endpoint_path (List[str]): List of the endpoint names that make the path of the
            corresponding api class (eg. ["sources", "virtual-channel"])
        with_content_commands (bool | List[str]): Defines whether the group contains
            commands for handling resource content (for sources and services)
        extra_commands (list): List of additional commands to add

    Returns:
        cloup.Group: The MultiCommand group with all its nested commands
    """
    resource_title = title if title else str.title(name.replace("-", " "))
    root_resource = endpoint_path[0]
    if len(endpoint_path) > 1:
        parent_resource_title = re.sub("s$", "", endpoint_path[0])
        resource_title = f"{resource_title} {parent_resource_title}"

    resource_title_plural = (
        f"{resource_title}s"
        if resource_title[-1] != "y"
        else f"{resource_title[:-1]}ies"
    )

    sections = []

    # === HELPER functions ===
    # Moved to click_helpers

    # === GROUP ===

    @cloup.group(
        name=name,
        help=f"Manage {resource_title_plural}",
        aliases=aliases,
        cls=bic_res_cmd.ResourceGroup,
        show_subcommand_aliases=True,
        resource_type=resource_type,
    )
    # The --id option is actually completely ignored, and redundant with the argument
    # (which itself is manipulated by the ApiResourceGroup class)
    # It's here mainly to allow auto-completion (OhMyZsh, Fig, etc)
    @click.option(
        "-i",
        "--id",
        help=f"Identifier of the {resource_title}. "
        "It is an alternative to providing it directly as an argument, "
        "and is mainly used for auto-completion purposes.",
        metavar=f"<{name}-id>",
    )
    @cloup.argument(
        "id",
        metavar=f"<{name}-id>",
        help=(
            f"The identifier of the {resource_title} to work with. "
            f"Leave empty for commands operating on a list of {resource_title_plural}. "
            "You can use $ and @ notation to refer to previously selected resources."
        ),
    )
    @click.pass_context
    @SessionRecorder.do_not_record
    def resource_group(ctx, id):
        if id and id != bic_res_cmd.ARG_TO_IGNORE:
            resource = retrieve_api_resource_from_chain(id, endpoint_path=endpoint_path)
            if ctx.invoked_subcommand != "get":
                display_resource_info(resource)

    # === CRUD Commands ===

    # --- LIST Command
    @bic_res_cmd.command(
        help=f"List all {resource_title_plural}",
        aliases=["ls"],
        is_default=True,
        takes_id_arg=False,
    )
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.pass_obj
    def list(
        obj: AppContext, list_format, select_fields, sort_fields, id_only, return_first
    ):
        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.list()

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            id_only=id_only,
            return_first=return_first,
        )

    # --- GET Commmand
    @bic_res_cmd.command(
        aliases=["retrieve", "json"],
        is_default=True,
        takes_id_arg=True,
        help=f"Get the JSON representation of a single {resource_title} by ID",
    )
    @click.option(
        "--save",
        is_flag=True,
        default=False,
        help=f"Save the {resource_title} payload into a JSON file",
    )
    @click.pass_obj
    def get(obj: AppContext, save: bool):
        resource = obj.current_resource

        obj.response_handler.treat_single_resource(resource, format="json")

        if save:
            save_resource(resource)

    # --- SEARCH Command
    @bic_res_cmd.command(
        help=f"Retrieve a list of all {resource_title_plural} "
        "that match given terms in all or selected fields",
        takes_id_arg=False,
    )
    @bic_options.search
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.pass_obj
    def search(
        obj: AppContext,
        single_term,
        search_terms,
        search_fields,
        sort_fields,
        list_format,
        select_fields,
        id_only,
        return_first,
    ):
        search_def = bic_options.validate_search(
            single_term, search_terms, search_fields
        )

        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.search(filters=search_def)

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            id_only=id_only,
            return_first=return_first,
        )

    # --- DELETE Commmand
    @bic_res_cmd.command(
        aliases=["del"],
        help=f"Delete a specific {resource_title} by ID",
        takes_id_arg=True,
    )
    @click.confirmation_option(prompt="Are you sure you want to delete this resource?")
    @click.pass_context
    def delete(ctx):
        resource = ctx.obj.current_resource

        endpoint = get_api_endpoint(endpoint_path)
        endpoint.delete(resource.id)

        # remove from cache
        ctx.obj.cache.remove(resource)

        click.secho(f"Resource {resource.id} deleted", fg="green")

    # --- EDIT Command
    @bic_res_cmd.command(help=f"Edit a {resource_title} (JSON) and update it")
    @click.pass_context
    def edit(ctx):
        resource = ctx.obj.current_resource
        resource_id = resource.id

        # remap to an input model
        resource = mappings.to_input_model(resource)

        updated_resource = edit_payload(resource)

        endpoint = get_api_endpoint(endpoint_path)
        # TODO - try to parse into the resource class (otherwise can only work with specific resource sub-types)
        endpoint.update(resource_id, updated_resource)

        click.secho(f"Resource {resource_id} updated", fg="green")

    # --- UPDATE Command
    @bic_res_cmd.command(
        aliases=["put"], help=f"Update a single property of a {resource_title}"
    )
    @cloup.argument(
        "property",
        help="Property that needs to be updated. Use dot notation for nested properties",
        required=True,
    )
    @cloup.argument("value", help="New value for the property", required=False)
    @cloup.option("--null", help="Remove the property", flag_value=True)
    @click.pass_context
    def update(ctx, property: str, value, null):
        if value == "-":
            value = click.get_text_stream("stdin").read()

        if not (null or value):
            raise BroadpeakIoCliError(
                "You must provide a value when updating a specific property"
            )

        resource = ctx.obj.current_resource
        resource_id = resource.id

        # remap to an input model
        resource = mappings.to_input_model(resource)

        updated_resource = edit_property(
            resource, property, "__NULL__" if null else value
        )

        endpoint = get_api_endpoint(endpoint_path)
        # TODO - try to parse into the resource class (otherwise can only work with specific resource sub-types)
        endpoint.update(resource_id, updated_resource)

        click.secho(f"Resource {resource_id} updated", fg="green")

    # --- DUPLICATE Command
    @bic_res_cmd.command(aliases=["copy"], help=f"Duplicate a {resource_title}")
    @click.option(
        "-e",
        "--edit",
        help="Edit the duplicated resource before saving it",
        is_flag=True,
        default=False,
    )
    @click.option(
        "--name",
        help=f"Set the name for the duplicate {resource_title}",
        default=None,
    )
    @click.pass_obj
    def duplicate(obj: AppContext, edit: bool, name: str):
        resource = obj.current_resource
        endpoint = obj.api.root_endpoint_for_resource(resource)

        resource.name = name or resource.name + " (copy)"

        # remap to an input model
        resource = mappings.to_input_model(resource)

        if edit:
            resource = edit_payload(resource)

        new_resource = endpoint.create(resource)

        obj.response_handler.treat_single_resource(new_resource, format="json")

    sections.append(
        cloup.Section(
            "CRUD commands", [get, list, search, delete, edit, update, duplicate]
        )
    )

    # === SERVICE Commands ===
    service_section = cloup.Section("Service commands", [])

    if issubclass(resource_type, ServiceIn):
        # --- PAUSE Command
        @bic_res_cmd.command(aliases=["disable"], help="Disable (pause) a service")
        @click.pass_obj
        def pause(obj: AppContext):
            resource = obj.current_resource
            if resource.state == "paused":
                click.secho("Service state is already paused", fg="red")
            else:
                endpoint = obj.api.root_endpoint_for_resource(resource)

                updated_resource = endpoint.pause(resource.id)
                click.secho("Service state: ", fg="yellow", nl=False)
                click.secho(updated_resource.state, fg="yellow", bold=True)

        @bic_res_cmd.command(aliases=["enable"], help="Enable (unpause) a service")
        @click.pass_obj
        def unpause(obj: AppContext):
            resource = obj.current_resource
            if resource.state == "enabled":
                click.secho("Service state is already enabled", fg="red")
            else:
                endpoint = obj.api.root_endpoint_for_resource(resource)

                updated_resource = endpoint.unpause(resource.id)
                click.secho("Service state: ", fg="yellow", nl=False)
                click.secho(updated_resource.state, fg="yellow", bold=True)

        service_section.add_command(pause)
        service_section.add_command(unpause)

        sections.append(service_section)

    # === TRAVERSAL Commands ===
    # COMMAND: ID

    @bic_res_cmd.command(name="id", help="Extract the id (primarily useful chaining)")
    @click.pass_obj
    def extract_id(obj: AppContext, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        click.echo(resource.id)

    traversal_section = cloup.Section("Traversal commands", [extract_id])
    sections.append(traversal_section)

    # --- SELECT Commmand
    @bic_res_cmd.command(
        aliases=["set"],
        help=f"Select a specific {resource_title} to set the context on",
    )
    @click.pass_obj
    def select(obj: AppContext):
        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.list()

        def padid(s):
            o = f"({s})"
            return f"{o:<15}"

        choices = [
            dict(value=s, name=f"{s.id:>8}  {padid(s.type.value)}  -  {s.name}")
            for s in resources
        ]
        resource = prompt.fuzzy(message=f"Select a {resource_title}", choices=choices)

        obj.response_handler.treat_single_resource(resource)

    traversal_section.add_command(select)

    for new_command in traversal_commands:
        # if the command is a function (rather than a Command), we execute and pass context
        if callable(new_command) and not isinstance(new_command, click.Command):
            new_command = new_command(endpoint_path=endpoint_path)

        if not isinstance(new_command, builtins.list):
            new_command = [new_command]

        for new_cmd in new_command:
            traversal_section.add_command(new_cmd)

    # === CONTENT Commands ===

    content_section = cloup.Section("Content commands", [])

    if any(x in with_content_commands for x in ["all", "url"]):
        # --- URL Command
        @bic_res_cmd.command(help="Retrieve the full URL of the resource")
        @bic_options.url(for_service=(root_resource == "services"))
        @click.pass_obj
        def url(
            obj: AppContext,
            sub: int,
            query: List[str],
            header: List[str],
            user_agent: str,
            url: Optional[str] = None,
            fqdn: Optional[str] = None,
            session: Optional[str] = None,
            service_as_param: Optional[bool] = False,
            **kwargs,
        ):
            resource = obj.current_resource
            full_url = resource.make_full_url()

            console.print(
                Panel(
                    Text.from_ansi(
                        pretty_url(full_url, getattr(resource, "assetSample", None))
                    ),
                    expand=False,
                )
            )

            click.echo(full_url)

            # Then resolve it
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                additional_headers=header,
                subplaylist_index=sub,
                user_agent=user_agent,
                session=session,
                service_as_param=service_as_param,
            )

            if handler and handler.url != full_url:
                click.secho("\nCalculating resolved URL: ")
                console.print(
                    Panel(Text.from_ansi(pretty_url(handler.url)), expand=False)
                )
                click.echo(handler.url)

            obj.cache.record(parse_obj_as(HttpUrl, handler.url))

        content_section.add_command(url)

    if any(x in with_content_commands for x in ["all", "check"]):
        # --- CHECK Command
        @bic_res_cmd.command(
            help="Check the validity of a Source (or Source associated with a Service)"
        )
        @click.option(
            "--full",
            help="Provide the full detail (in JSON)",
            is_flag=True,
            default=False,
        )
        @click.pass_obj
        def check(
            obj: AppContext,
            full: bool,
            **kwargs,
        ):
            resource = obj.current_resource
            id = obj.current_resource.id

            if isinstance(resource, ServiceIn):
                id = resource.main_source().id
                display_tip(f"Checking status for associated source with id {id}")

            result = obj.api.sources.check_by_id(id)

            display_source_status(obj, result, as_json=full)

        content_section.add_command(check)

    if any(x in with_content_commands for x in ["all", "info"]):
        # --- INFO Commmand
        @bic_res_cmd.command(
            aliases=["content"],
            help=f"Get detailed information about a specific {resource_title} by ID",
        )
        @bic_options.url(for_service=(root_resource == "services"))
        @click.option(
            "--content/--no-content",
            "with_content",
            is_flag=True,
            default=True,
            help="Add or hide summary information about the content of the resource",
        )
        @click.pass_context
        def info(
            ctx,
            sub: int,
            query: List[str],
            header: List[str],
            user_agent: str,
            with_content: bool = True,
            url: Optional[str] = None,
            fqdn: Optional[str] = None,
            session: Optional[str] = None,
            **kwargs,
        ):
            resource = ctx.obj.current_resource

            ctx.obj.response_handler.treat_single_resource(resource)

            # then show the summary table (if there is one)
            if with_content:
                handler = get_content_handler(
                    resource,
                    replacement_fqdn=fqdn,
                    extra_url=url,
                    additional_query_params=query,
                    additional_headers=header,
                    subplaylist_index=sub,
                    user_agent=user_agent,
                    session=session,
                )
                if handler:
                    try:
                        display_content(
                            handler=handler,
                            max=1,
                            interval=0,
                            table=True,
                            trim=0,
                        )
                    except BroadpeakIoCliError:
                        pass

        content_section.add_command(info)

    if any(x in with_content_commands for x in ["all", "read"]):
        # --- READ Command
        @bic_res_cmd.command(
            help=f"Load and display the content of a {resource_title}"
            ", optionally highlighted with relevant information"
        )
        @bic_options.url(for_service=(root_resource == "services"))
        @bic_options.read
        @bic_options.table
        @bic_options.dash
        @click.pass_obj
        def read(
            obj: AppContext,
            sub: int,
            query: List[str],
            header: List[str],
            user_agent: str,
            table: bool,
            timeline: bool,
            raw: bool,
            ad_pattern: str,
            trim: int = 0,
            top: int = 0,
            tail: int = 0,
            pager: bool = False,
            url: Optional[str] = None,
            fqdn: Optional[str] = None,
            session: Optional[str] = None,
            service_as_param: Optional[bool] = False,
            **kwargs,
        ):
            resource = obj.current_resource
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                additional_headers=header,
                subplaylist_index=sub,
                user_agent=user_agent,
                session=session,
                service_as_param=service_as_param,
            )
            if handler:
                try:
                    display_content(
                        handler=handler,
                        max=1,
                        interval=0,
                        table=table,
                        raw=raw,
                        top=top,
                        tail=tail,
                        pager=pager,
                        trim=trim,
                        ad_pattern=ad_pattern,
                        timeline=timeline,
                        **kwargs,
                    )
                except BroadpeakIoCliError:
                    pass

        content_section.add_command(read)

    if any(x in with_content_commands for x in ["all", "poll"]):
        # --- POLL Command
        @bic_res_cmd.command(
            help=f"Similar to `read`, but regularly re-load the {resource_title}"
            "source's content"
        )
        @bic_options.poll
        @bic_options.read
        @bic_options.url(for_service=(root_resource == "services"))
        @bic_options.table
        @bic_options.dash
        @click.pass_obj
        def poll(
            obj: AppContext,
            sub: int,
            query: List[str],
            header: List[str],
            user_agent: str,
            max: int,
            interval: Optional[int],
            raw: bool,
            diff: bool,
            top: bool,
            tail: bool,
            clear: bool,
            table: bool,
            timeline: bool,
            pager: bool,
            silent: bool,
            ad_pattern: str,
            trim: int,
            url: Optional[str] = None,
            fqdn: Optional[str] = None,
            session: Optional[str] = None,
            service_as_param: Optional[bool] = False,
            **kwargs,
        ):
            resource = obj.current_resource

            if not resource.is_live():
                raise BroadpeakIoCliError(
                    "Polling can only be done for Live resources (sources or services)"
                )

            if resource.format == MediaFormat.HLS:
                if not sub:
                    sub = 1
                    click.secho(
                        CL.warning(
                            "With HLS, poll is only meaningful with sub-playlists. "
                            "Use `--sub N` to choose one. Selecting first one by default"
                        )
                    )

            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                additional_headers=header,
                subplaylist_index=sub,
                user_agent=user_agent,
                session=session,
                service_as_param=service_as_param,
            )

            if handler:
                display_content(
                    handler,
                    max=max,
                    interval=interval,
                    table=table,
                    raw=raw,
                    diff=diff,
                    top=top,
                    tail=tail,
                    clear=clear,
                    pager=pager,
                    silent=silent,
                    trim=trim,
                    ad_pattern=ad_pattern,
                    timeline=timeline,
                    **kwargs,
                )

        content_section.add_command(poll)

    if any(x in with_content_commands for x in ["all", "monitor"]):
        # --- MONITOR Command
        @bic_res_cmd.command(help="Check a live stream for significant markers")
        @bic_options.url(for_service=(root_resource == "services"))
        @bic_options.read
        @bic_options.poll
        @bic_options.monitor
        @click.pass_obj
        def monitor(
            obj: AppContext,
            query: List[str],
            header: List[str],
            user_agent: str,
            sub: int,
            max: int,
            interval: Optional[int],
            silent: bool,
            save: bool,
            with_schedule: bool,
            with_map: bool,
            with_signals: bool,
            with_adinfo: bool,
            with_frames: bool,
            ad_pattern: str,
            fqdn: Optional[str] = None,
            url: Optional[str] = None,
            session: Optional[str] = None,
            service_as_param: Optional[bool] = False,
            **kwargs,
        ):
            resource = obj.current_resource
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                additional_query_params=query,
                additional_headers=header,
                subplaylist_index=sub,
                user_agent=user_agent,
                session=session,
                service_as_param=service_as_param,
            )

            if not resource.is_live():
                raise BroadpeakIoCliError(
                    "Monitoring can only be done for Live resources (sources or services)"
                )

            if isinstance(handler, DASHHandler):
                raise NotImplementedError(
                    "Monitoring of DASH streams not yet implemented in BIC"
                )

            if isinstance(handler, HLSHandler) and handler.has_children():
                handler = handler.get_child(1)
                monitor_hls(
                    handler=handler,
                    max=max,
                    interval=interval,
                    silent=silent,
                    name=resource.summary,
                    save_to_file=save,
                    with_schedule=with_schedule,
                    with_map=with_map,
                    with_signals=with_signals,
                    with_adinfo=with_adinfo,
                    with_frames=with_frames,
                    ad_pattern=ad_pattern,
                )

        content_section.add_command(monitor)

    if any(x in with_content_commands for x in ["all", "play"]):
        # --- PLAY Command
        @bic_res_cmd.command(
            help=f"Open the URL of the {resource_title} in a web player",
            aliases=["open"],
        )
        @bic_options.url(for_service=(root_resource == "services"))
        @click.option(
            "-p",
            "--player",
            default="CONFIG",
            help="The label for a player URL template",
            metavar="<player-label>",
            type=str,
            is_flag=False,
            flag_value="CHOICE",
        )
        @click.option(
            "--start-session / --no-start-session",
            "start_session",
            help="[Services only] Resolve the URL to create a session first. "
            "This is useful to get session ID info in the terminal before starting play",
            is_flag=True,
            required=False,
            default=True,
            show_default=True,
        )
        @click.pass_obj
        def play(
            obj: AppContext,
            query: List[str],
            header: List[str],
            user_agent: str,
            sub: int,
            player: str,
            start_session: bool,
            fqdn: Optional[str] = None,
            url: Optional[str] = None,
            session: Optional[str] = None,
            service_as_param: Optional[bool] = False,
            **kwargs,
        ):
            resource = obj.current_resource
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
                additional_query_params=query,
                additional_headers=header,
                session=session,
                service_as_param=service_as_param,
            )
            if player == "CONFIG":
                player = obj.config.get("default-player")

            if player == "CHOICE":
                player = StreamPlayer.prompt_player()

            # pass a set of useful parameters for placeholder replacement
            # in the player template

            if hasattr(resource, "get_all_fields_and_properties"):
                params = resource.get_all_fields_and_properties()
            else:
                params = dict(params)

            # if service, retrieve the Location from the 307 redirect (to get session id)
            # For that, we just need to retrieve the content
            if isinstance(resource, ServiceIn) and start_session:
                _ = handler.content
                display_bpkio_session_info(handler)

            params.update(stream_url=handler.url)

            StreamPlayer().launch(key=player, **params)

        content_section.add_command(play)

    if any(x in with_content_commands for x in ["all", "download"]):
        # --- DOWNLOAD Command
        @bic_res_cmd.command(help=f"Download the {resource_title} to a local folder")
        @cloup.argument(
            "output_path",
            help="Local path to save the downloaded stream",
            type=str,
            default=None,
            required=False,
        )
        @bic_options.read
        @bic_options.url()
        @cloup.option(
            "-s",
            "--segments",
            "num_segments",
            help="Number of segments to download",
            type=int,
            default=0,
        )
        @click.pass_obj
        def download(
            obj: AppContext,
            sub: int,
            url: str,
            query: List[str],
            header: List[str],
            user_agent: str,
            session: Optional[str] = None,
            fqdn: Optional[str] = None,
            output_path: Optional[str] = None,
            num_segments: int = 0,
            **kwargs,
        ):
            resource = obj.current_resource
            handler = get_content_handler(
                resource,
                replacement_fqdn=fqdn,
                extra_url=url,
                subplaylist_index=sub,
                user_agent=user_agent,
                additional_query_params=query,
                additional_headers=header,
                session=session,
            )
            prefix = f"{resource.__class__.__name__}_{resource.id}"
            
            if not output_path:
                # Create a folder name with the current date and time
                output_path = f"{prefix}_download_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

            # Make a progressbar with Rich
            with Progress() as progress:        
                task = progress.add_task("Downloading...", total=None)

                def update_progress(message, total=None):
                    if total is not None:
                        progress.update(task, description=message, total=total)
                    else:
                        progress.update(task, description=message, advance=1)
                        time.sleep(0.2)  # just to allow it to update

                handler.download(output_path=output_path, num_segments=num_segments, progress_callback=update_progress)

            click.secho(CL.ok(f"Downloaded manifest to {output_path}"))
        
        content_section.add_command(download)

    if any(x in with_content_commands for x in ["all", "profile"]):
        if issubclass(resource_type, SourceIn):
            # --- PROFILE Command
            @bic_res_cmd.command(help=f"Create a profile from the {resource_title}")
            @click.option(
                "--save",
                is_flag=True,
                default=False,
                help="Save the profile to a file",
            )
            @click.option(
                "--name",
                type=str,
                default="",
                help="Name for the transcoding profile",
            )
            @click.option(
                "--schema",
                type=str,
                default="bkt-v2.1",
                help="Version of the transcoding profile schema",
            )
            @bic_options.url(for_service=(root_resource == "services"))
            @click.pass_obj
            def profile(
                obj: AppContext,
                query: List[str],
                header: List[str],
                user_agent: str,
                sub: int,
                save: bool,
                schema: str,
                name: str,
                fqdn: Optional[str] = None,
                url: Optional[str] = None,
                session: Optional[str] = None,
            ):
                resource = obj.current_resource
                handler = get_content_handler(
                    resource,
                    replacement_fqdn=fqdn,
                    extra_url=url,
                    subplaylist_index=sub,
                    user_agent=user_agent,
                    additional_query_params=query,
                    additional_headers=header,
                    session=session,
                )

                (profile, messages) = make_transcoding_profile(
                    handler, schema_version=schema, name=name
                )

                obj.response_handler.treat_single_resource(profile, format="json")

                if save:
                    filename = f"TranscodingProfileContent_from_{resource.__class__.__name__}_{resource.id}"
                    save_json(profile, filename, "Profile configuration")

                if messages:
                    for message in messages:
                        msg = message.message
                        if message.topic != "-":
                            msg = f"({message.topic})  {message.message}"
                        click.echo(CL.log(msg, message.level), err=True)
                    click.secho(
                        "Since errors or warnings have been raised, you may want to review the profile payload to ensure it is usable",
                        fg="yellow",
                        err=True,
                    )

            content_section.add_command(profile)

    sections.append(content_section)

    # === PACKAGE Commands

    # COMMAND: PACKAGE
    @bic_res_cmd.command()
    @cloup.option(
        "--save", "output_file", type=click.File("w"), required=False, default=None
    )
    @click.pass_obj
    def package(obj: AppContext, output_file):
        """Package a service and all its dependencies into a reusable recipe

        Args:
            output (str): Filename of the JSON file to write the package into
        """
        resource = obj.current_resource

        package_resources([resource], obj.api, output_file)

    sections.append(cloup.Section("Other commands", [package]))

    # === EXTRA Commands
    # Go through extra commands and add them where relevant...

    for new_command in extra_commands:
        # if the command is a function (rather than a Command), we execute and pass context
        if callable(new_command) and not isinstance(new_command, click.Command):
            new_command = new_command(endpoint_path=endpoint_path)

        if not isinstance(new_command, builtins.list):
            new_command = [new_command]

        for new_cmd in new_command:
            inserted = False
            for section in sections:
                for k in section.commands.keys():
                    if k == new_cmd.name:
                        # ... override an existing one ...
                        section.commands[k] = new_command
                        inserted = True
            if not inserted:
                # ... or add it to the last section
                if new_cmd.name in ["create", "update", "delete"]:
                    for section in sections:
                        if section.title == "CRUD commands":
                            section.add_command(new_cmd)
                            break
                else:
                    sections[-1].add_command(new_cmd)

    # === END OF GROUP ===
    for section in sections:
        resource_group.add_section(section)

    return resource_group
