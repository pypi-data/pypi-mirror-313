import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.models.BkpioSession import BpkioSession
from bpkio_api.models.Services import ServiceIn
from bpkio_cli.click_mods.resource_commands import (ARG_TO_IGNORE,
                                                    ResourceSubCommand)
from bpkio_cli.core.app_context import AppContext
from rich import print

default_fields = ["id", "service_id", "first_seen", "last_seen", "context"]


@bic_res_cmd.group(
    help="Manage playback sessions (captured automatically or specified explicitly)",
    resource_type=BpkioSession,
    aliases=[
        "sessions",
        "sess",
    ],
)
@cloup.argument(
    "session_id",
    help=("The session to work with"),
    required=False,
    metavar="<session-id>",
)
@cloup.pass_obj
def session(obj: AppContext, session_id: str):
    if session_id and session_id != ARG_TO_IGNORE:
        # lookup from cache to see if we've seen before
        previous_sessions = obj.cache.list_resources_by_type(BpkioSession)

        # if in the context of a service, check that it belongs to that service
        if parent := obj.resource_chain.parent():
            if isinstance(parent[1], ServiceIn):
                previous_sessions = [
                    s for s in previous_sessions if s.service_id == parent[1].hash
                ]

        session = next((s for s in previous_sessions if session_id in s.id), None)

        if not session:
            if parent and previous_sessions:
                raise ValueError(f"Session {session_id} was not found for this service")
            else:
                raise ValueError(f"Session {session_id} not found")

        # and update the resource trail
        obj.resource_chain.overwrite_last(session_id, session)


@session.command(
    name="print",
    takes_id_arg=True,
    is_default=True,
    help="Print it",
)
@cloup.pass_obj
def show(obj: AppContext):
    session = obj.current_resource
    print(session)


# --- LIST Command
@session.command(
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

    sessions = obj.cache.list_resources_by_type(BpkioSession)

    # filter in case called from service context
    if isinstance(obj.current_resource, ServiceIn):
        sessions = [s for s in sessions if s.service_id == obj.current_resource.hash]

    obj.response_handler.treat_list_resources(
        sessions,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )
