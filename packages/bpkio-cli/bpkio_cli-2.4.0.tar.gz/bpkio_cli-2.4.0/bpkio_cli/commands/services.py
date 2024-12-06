import click
import cloup
from bpkio_api.models import (
    AdaptiveStreamingCdnService,
    AdaptiveStreamingCdnServiceIn,
    AdInsertionService,
    ContentReplacementService,
    ContentReplacementSlot,
    ServiceIn,
    VirtualChannelService,
    VirtualChannelSlot,
)

from bpkio_cli.commands.creators.ad_insertion import create_ad_insertion_service_command
from bpkio_cli.commands.creators.services import create_service_command
from bpkio_cli.commands.creators.slot_iterators import (
    clear_slots_command,
    replicate_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel import (
    create_virtual_channel_service_command,
)
from bpkio_cli.commands.creators.virtual_channel_populate import (
    populate_virtual_channel_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel_slot import create_slot_command
from bpkio_cli.commands.sessions import session
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.commands.template_crud_slots import create_child_resource_group
from bpkio_cli.core.api_resource_helpers import retrieve_api_resource_from_chain
from bpkio_cli.core.app_context import AppContext

default_fields = ["id", "name", "type", "hash", "state", "format"]


def get_services_commands():
    root_endpoint = "services"
    root: cloup.Group = create_resource_group(
        "service",
        resource_type=ServiceIn,
        endpoint_path=[root_endpoint],
        aliases=["svc", "services"],
        with_content_commands=["all"],
        default_fields=default_fields,
        traversal_commands=[source_commands],
        extra_commands=[
            hash_command,
            session,
            create_service_command(),
        ],
    )

    return [
        root,
        create_resource_group(
            "content-replacement",
            resource_type=ContentReplacementService,
            endpoint_path=[root_endpoint, "content_replacement"],
            aliases=["cr"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                clear_slots_command(),
                replicate_slots_command(),
                add_slots_commands(
                    resource_type=ContentReplacementSlot,
                    parent_path=[root_endpoint, "content_replacement"],
                    default_fields=[
                        "id",
                        "name",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                    ],
                ),
            ],
        ),
        create_resource_group(
            "ad-insertion",
            resource_type=AdInsertionService,
            endpoint_path=[root_endpoint, "ad_insertion"],
            aliases=["dai", "ssai"],
            default_fields=[
                "id",
                "name",
                "type",
                "sub_type",
                "hash",
                "state",
                "format",
            ],
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                create_ad_insertion_service_command(),
            ],
        ),
        create_resource_group(
            "virtual-channel",
            resource_type=VirtualChannelService,
            endpoint_path=[root_endpoint, "virtual_channel"],
            aliases=["vc"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                hash_command,
                session,
                clear_slots_command(),
                create_virtual_channel_service_command(),
                populate_virtual_channel_slots_command(),
                replicate_slots_command(),
                add_slots_commands(
                    resource_type=VirtualChannelSlot,
                    parent_path=[root_endpoint, "virtual_channel"],
                    default_fields=[
                        "id",
                        "name",
                        "type",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                        "category.id",
                        "category.name",
                    ],
                    extra_commands=[create_slot_command()],
                ),
            ],
        ),
        create_resource_group(
            "adaptive-streaming-cdn",
            resource_type=AdaptiveStreamingCdnService,
            endpoint_path=[root_endpoint, "adaptive_streaming_cdn"],
            aliases=["cdn"],
            default_fields=default_fields,
            extra_commands=[
                hash_command,
            ],
        ),
    ]


def add_slots_commands(resource_type, parent_path, default_fields, extra_commands=[]):
    return create_child_resource_group(
        "slot",
        resource_type=resource_type,
        endpoint_path=parent_path + ["slots"],
        aliases=["slots"],
        default_fields=default_fields,
        extra_commands=extra_commands,
    )


# COMMAND: HASH
def hash_command(endpoint_path: str):
    @cloup.command(help="Show the service hash (bpkio_serviceid)")
    @click.pass_obj
    def hash(obj: AppContext, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        click.echo(resource.hash)

    return hash


def source_commands(endpoint_path: str):
    # COMMAND: SOURCE
    @cloup.command(help="Select the main source used by the service", aliases=["src"])
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def source(obj: AppContext, id_only, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        # then get the full service
        resource = obj.api.services.retrieve(resource.id)

        source = None
        if hasattr(resource, "source"):
            source = obj.api.sources.retrieve(resource.source.id)
        elif hasattr(resource, "baseLive"):
            source = obj.api.sources.retrieve(resource.baseLive.id)

        obj.response_handler.treat_single_resource(source, id_only=id_only)

    # COMMAND: ADS
    @cloup.command(
        help="Select the ad server behind the service",
        name="ad-server",
        aliases=["ads"],
    )
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def ad_server(obj: AppContext, id_only, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        source = None
        keys = [
            "vodAdInsertion",
            "adBreakInsertion",
            "liveAdPreRoll",
            "liveAdReplacement",
        ]
        for k in keys:
            if hasattr(resource, k):
                o = getattr(resource, k)
                if o is not None:
                    click.secho("Ad server for: " + k)
                    source = obj.api.sources.retrieve(o.adServer.id)
                    obj.response_handler.treat_single_resource(source, id_only=id_only)
                    # return source

        if not source:
            click.secho("This service has no ad server")

    # COMMAND: PROFILE
    @cloup.command(
        help="Select the ad server behind the service",
        name="transcoding-profile",
        aliases=["profile", "prf"],
    )
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def profile(obj: AppContext, id_only, **kwargs):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        if (
            hasattr(resource, "transcodingProfile")
            and resource.transcodingProfile is not None
        ):
            id = resource.transcodingProfile.id
            if id is not None:
                profile = obj.api.transcoding_profiles.retrieve(id)
                obj.response_handler.treat_single_resource(profile, id_only=id_only)
                return profile

        click.secho("This service has no transcoding profile")

    # COMMAND: DEPENDENCIES
    @cloup.command(
        help="Select the (primary) dependencies of the service",
        name="dependencies",
        aliases=["deps"],
    )
    @click.pass_context
    def dependencies(ctx, **kwargs):
        ctx.forward(source)
        ctx.forward(ad_server)
        ctx.forward(profile)

    return [source, ad_server, profile, dependencies]
