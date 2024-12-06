from urllib.parse import parse_qs, urlparse

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.utils.prompt as prompt
import click
from bpkio_api.models import SourceType, VirtualChannelServiceIn
from bpkio_api.models.Services import AdvancedOptions, QueryManagement
from bpkio_cli.commands.creators.virtual_channel_populate import \
    populate_virtual_channel_slots_with_prompts
from bpkio_cli.core.app_context import AppContext


def create_virtual_channel_service_command():
    # COMMAND: CREATE
    @bic_res_cmd.command(
        help="Create a (simple) Virtual Channel service", takes_id_arg=False
    )
    @click.pass_obj
    def create(obj: AppContext):
        create_virtual_channel_service_with_prompts(obj)

    return create


def create_virtual_channel_service_with_prompts(obj: AppContext):
    all_sources = obj.api.sources.list()

    # Ask for the live source
    live_sources = [s for s in all_sources if s.type == SourceType.LIVE]
    live_sources = sorted(live_sources, key=lambda s: s.id, reverse=True)
    live_sources = obj.cache.sort_resources_by_most_recently_accessed(live_sources)
    choices = [
        dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]")
        for s in live_sources
    ]
    live_source_id = prompt.fuzzy(message="Source", choices=choices)

    # Extract the query params from the live source
    live_source = next(s for s in live_sources if s.id == live_source_id)
    live_source_url = urlparse(live_source.url)
    live_source_url_params = list(parse_qs(live_source_url.query).keys())
    click.echo(f"Query parameters to forward to origin: {live_source_url_params}")

    # Then ask for the ad server
    ad_sources = [s for s in all_sources if s.type == SourceType.AD_SERVER]
    ad_sources = sorted(ad_sources, key=lambda s: s.id, reverse=True)
    ad_sources = obj.cache.sort_resources_by_most_recently_accessed(ad_sources)
    choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in ad_sources]
    choices = [dict(value=None, name="-- No ad insertion --")] + choices
    ad_source_id = prompt.fuzzy(message="Ad Server", choices=choices)

    slate_source_id = None
    transcoding_profile_id = None

    if ad_source_id:
        # Then ask for the gap filler
        slate_sources = [s for s in all_sources if s.type == SourceType.SLATE]
        slate_sources = sorted(slate_sources, key=lambda s: s.id, reverse=True)
        slate_sources = obj.cache.sort_resources_by_most_recently_accessed(
            slate_sources
        )
        choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in slate_sources]
        choices = [dict(value=None, name="-- No gap filler --")] + choices
        slate_source_id = prompt.fuzzy(message="Gap Filler", choices=choices)

        # Ask for transcoding profile
        profiles = obj.api.transcoding_profiles.list()
        profiles = obj.cache.sort_resources_by_most_recently_accessed(profiles)
        choices = [dict(value=s.id, name=f"{s.name} ({s.id})") for s in profiles]
        # ... add a "none" one, but only if transcoding can be bypassed
        if slate_source_id is None:
            choices = [dict(value=None, name="-- No transcoding --")] + choices

        transcoding_profile_id = prompt.fuzzy(
            message="Transcoding Profile", choices=choices
        )

    # Ask for other options
    name = prompt.text(
        message="Name",
        validate=lambda result: len(result) > 0,
        invalid_message="The name cannot be empty.",
    )

    with_transcoding = transcoding_profile_id is not None

    # Create the service object
    service = VirtualChannelServiceIn(
        name=name,
        baseLive=dict(id=live_source_id),
    )

    if live_source_url_params:
        service.advancedOptions = AdvancedOptions(
            queryManagement=QueryManagement(
                forwardInOriginRequest=live_source_url_params,
                addToHLSMediaPlaylistURI=[],
                addToMediaSegmentURI=[],
            ),
        )

    if ad_source_id:
        ad_insertion = dict(adServer=dict(id=ad_source_id))
        if slate_source_id is not None:
            ad_insertion["gapFiller"] = dict(id=slate_source_id)

        service.adBreakInsertion = ad_insertion

        if with_transcoding:
            service.enableAdTranscoding = True
            service.transcodingProfile = dict(id=transcoding_profile_id)

    service_out = obj.api.services.virtual_channel.create(service)

    obj.response_handler.treat_single_resource(service_out)

    # Optionally populate with slots
    do_populate = prompt.confirm("Would you like to populate this service with slots?")

    if do_populate:
        populate_virtual_channel_slots_with_prompts(obj, service_out.id, categories=[])

    return service_out
