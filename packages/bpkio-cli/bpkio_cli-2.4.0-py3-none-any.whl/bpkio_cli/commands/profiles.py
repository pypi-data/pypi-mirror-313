import json as j

import bpkio_api.models as models
import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder, SessionSection
from bpkio_api.models import TranscodingProfile
from bpkio_cli.core.api_resource_helpers import \
    retrieve_api_resource_from_chain
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.response_handler import save_json, save_resource
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.tables import display_table

default_fields = ["id", "name", "layers"]


# # --- TRANSCODING PROFILES Group
@bic_res_cmd.group(
    aliases=["prf", "profiles", "transcoding-profile"],
    show_subcommand_aliases=True,
    resource_type=TranscodingProfile,
)
@cloup.argument(
    "profile_id",
    metavar="<profile-id>",
    help=(
        "The identifier of the transcoding profile to work with. "
        "Leave empty for commands operating on a list of profiles."
    ),
)
@click.pass_obj
def profile(obj, profile_id: str):
    """Manage Transcoding Profiles"""

    @SessionRecorder.do_not_record
    def show_breadcrumb():
        if profile_id and profile_id != bic_res_cmd.ARG_TO_IGNORE:
            # TODO - find a way of passing the target tenant (admin mode)
            profile = retrieve_api_resource_from_chain(
                profile_id, endpoint_path=["transcoding_profiles"]
            )
            display_resource_info(profile)

    show_breadcrumb()


# --- LIST Command
@bic_res_cmd.command(
    help="Retrieve a list of all Transcoding Profiles",
    aliases=["ls"],
    name="list",
    is_default=True,
    takes_id_arg=False,
)
@bic_options.list(default_fields=default_fields)
@bic_options.output_formats
@click.pass_obj
def lst(
    obj: AppContext,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
):
    SessionRecorder.record(
        SessionSection(
            title="List of Transcoding Profiles", description="This is for a test"
        )
    )

    profiles = obj.api.transcoding_profiles.list()

    obj.response_handler.treat_list_resources(
        profiles,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )


# --- INFO Command
@bic_res_cmd.command(
    help="Retrieve detailed info about a single Transcoding Profile, by its ID",
)
@click.option(
    "--content/--no-content",
    "with_content",
    is_flag=True,
    default=True,
    help="Add or hide summary information about the content of the resource",
)
@click.pass_obj
def info(obj: AppContext, with_content):
    profile = obj.current_resource

    obj.response_handler.treat_single_resource(profile)

    def simplify_fractions(d):
        for k, v in d.items():
            if isinstance(v, dict) and v.get("num") is not None:
                d[k] = str(v.get("num"))
                if v.get("den") != 1:
                    d[k] += f"/{v.get('den')}"

    if with_content:
        packaging_info = profile.json_content["packaging"]
        advanced_info = packaging_info.pop("advanced", None)
        if advanced_info:
            packaging_info.update(
                {k.replace("--", ""): v for k, v in advanced_info.items()}
            )
        simplify_fractions(packaging_info)

        # if packaging_info[]

        display_table(packaging_info)

        renditions = []
        for media in ["videos", "audios"]:
            profile_rends = profile.json_content[media]
            common = profile_rends.pop("common", {})
            for vid in profile_rends.values():
                for k, v in common.items():
                    vid.setdefault(k, v)
                    simplify_fractions(vid)
                renditions.append(vid)

        display_table(renditions)


# --- ID Command
@bic_res_cmd.command(
    name="id",
    help="Return the ID of the resource",
)
@click.pass_obj
def extract_id(obj: AppContext):
    profile = obj.current_resource
    click.echo(profile.id)


# --- GET Command
@bic_res_cmd.command(
    aliases=["retrieve", "json"],
    help="Get the JSON representation of a single Transcoding Profile "
    "or list of Transcoding Profiles",
)
@click.option(
    "-c",
    "--content",
    "content_only",
    is_flag=True,
    default=False,
    help="Extract the actual profile's JSON and pretty print it",
)
@click.option(
    "--save",
    is_flag=True,
    default=False,
    help="Save the profile payload into a JSON file",
)
@click.pass_obj
def get(obj: AppContext, content_only, save):
    try:
        profile = obj.current_resource

        if content_only:
            profile = profile.json_content

        obj.response_handler.treat_single_resource(profile, format="json")

        if save:
            if content_only:
                save_json(
                    profile,
                    f"TranscodingProfileContent_{profile.id}",
                    "Profile configuration",
                )
            else:
                save_resource(profile)

    except Exception:
        profiles = obj.api.transcoding_profiles.list()
        if content_only:
            # TODO - Dirty code. Needs resolving, maybe at level of the SDK
            bare_profiles = []
            for profile in profiles:
                new_pro = j.loads(profile.json())
                new_pro["_expanded_content"] = profile.json_content
                bare_profiles.append(new_pro)
            profiles = bare_profiles

        obj.response_handler.treat_list_resources(
            profiles,
            format="json",
        )


# --- CONTENT Command
@bic_res_cmd.command(
    aliases=["display"],
    help="Display the JSON of the Transcoding Profile (as sent to BkT)",
    is_default=True,
)
@click.pass_context
def content(ctx: click.Context):
    ctx.invoke(get, content_only=True)


# --- SEARCH Command
@bic_res_cmd.command(
    help="Retrieve a list of all Transcoding Profiles that match given "
    "terms in all or selected fields",
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
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
):
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    profiles = obj.api.transcoding_profiles.search(filters=search_def)

    obj.response_handler.treat_list_resources(
        profiles,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )


# --- SELECT Commmand
@bic_res_cmd.command(
    aliases=["set"],
    help="Select a specific Transcoding Profile to set the context on",
)
@click.pass_obj
def select(obj: AppContext):
    profiles = obj.api.transcoding_profiles.list()

    choices = [dict(value=s, name=f"{s.id:>8}  -  {s.name}") for s in profiles]
    resource = prompt.fuzzy(message="Select a Transcoding Profile", choices=choices)

    obj.response_handler.treat_single_resource(resource)


# --- USAGE Command
@bic_res_cmd.command(help="Find all Services that use the profile")
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
    **kwargs,
):
    select_fields = list(select_fields)

    profile = obj.current_resource

    services = obj.api.services.list()

    selected_services = []
    for service in services:
        svc = obj.api.services.retrieve(service.id)

        if isinstance(svc, models.VirtualChannelService):
            if svc.transcodingProfile and svc.transcodingProfile.id == profile.id:
                selected_services.append(svc)

        if isinstance(svc, models.AdInsertionService):
            if svc.transcodingProfile and svc.transcodingProfile.id == profile.id:
                selected_services.append(svc)

    obj.response_handler.treat_list_resources(
        selected_services,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )


# --- ID Command


# ===

profile.add_section(cloup.Section("CRUD commands", [get, info, lst, search]))

profile.add_section(cloup.Section("Content commands", [content]))

profile.add_section(cloup.Section("Traversal commands", [extract_id, select, usage]))
