import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import click
import cloup
from bpkio_api.models import (VirtualChannelService, VirtualChannelSlotIn,
                              VirtualChannelSlotType)
from bpkio_api.models.common import BaseResource
from bpkio_api.models.Sources import AssetSource, LiveSource
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.commands.creators.virtual_channel_populate import \
    _get_duration_from_asset
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.utils.datetimes import (parse_date_expression_as_utc,
                                       parse_duration_expression)


def create_slot_command():
    # COMMAND: CREATE VC SLOT
    @bic_res_cmd.command(help="Quickly add a slot", takes_id_arg=False)
    @cloup.option_group(
        "Types of slots",
        cloup.option(
            "--ad",
            is_flag=True,
        ),
        cloup.option(
            "--source",
            "source_id",
            required=False,
            default=None,
            help="Source identifier",
            metavar="ID",
        ),
        constraint=cloup.constraints.mutually_exclusive,
    )
    @click.option(
        "--in",
        "slot_start",
        type=tuple,
        cls=OptionEatAll,
        default=("30 sec",),
        help="When the slot will start",
    )
    @click.option(
        "--for",
        "slot_duration",
        type=tuple,
        cls=OptionEatAll,
        default=None,
        help="Duration of the slot, defaulting to 1 min for ad slots, 5 min for live content, and natural duration for assets",
    )
    @click.pass_obj
    def create(obj: AppContext, ad, source_id, slot_start, slot_duration):
        vc_id = obj.resource_chain.last_key()
        create_vc_slot(
            obj,
            vc_id,
            slot_start,
            slot_duration,
            source_id=source_id,
            is_ad=ad,
        )

    return create


def create_vc_slot(
    context: AppContext, vc_id, break_start, break_duration, source_id=None, is_ad=False
):
    api = context.api
    vc: VirtualChannelService = api.services.virtual_channel.retrieve(vc_id)

    if break_start:
        start_time = parse_date_expression_as_utc(break_start, future=True)
    duration = None
    if break_duration:
        duration = parse_duration_expression(break_duration)

    if is_ad:
        slot = create_vc_ad_slot(api, vc.id, start_time, duration)
    else:
        if not source_id:
            raise BroadpeakIoCliError(
                "You must provide a source_id when using a content slot"
            )
        slot = create_vc_content_slot(api, vc.id, source_id, start_time, duration)

    context.response_handler.treat_single_resource(slot, format="json")


def create_vc_ad_slot(api, vc_id, start_time, duration):
    if not duration:
        duration = 60

    slot = VirtualChannelSlotIn(
        name="Ad Break (from bic)",
        startTime=start_time,
        duration=duration,
        type=VirtualChannelSlotType.AD_BREAK,
    )
    return api.services.virtual_channel.slots.create(vc_id, slot)


def create_vc_content_slot(
    api,
    vc_id,
    source_id,
    start_time,
    duration=None,
):
    source = api.sources.retrieve(source_id)

    if not duration:
        if isinstance(source, AssetSource):
            duration = _get_duration_from_asset(source.full_url)
        if isinstance(source, LiveSource):
            duration = 300

    slot = VirtualChannelSlotIn(
        name=source.name,
        startTime=start_time,
        duration=duration,
        type=VirtualChannelSlotType.CONTENT,
        replacement=BaseResource(id=source.id),
    )
    return api.services.virtual_channel.slots.create(vc_id, slot)
