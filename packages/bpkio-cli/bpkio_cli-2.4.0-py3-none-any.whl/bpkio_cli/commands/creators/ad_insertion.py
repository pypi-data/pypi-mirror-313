from urllib.parse import parse_qs, urlparse

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.utils.prompt as prompt
import click
from bpkio_api.models import AdInsertionServiceIn, SourceType
from bpkio_api.models.Services import (
    AdvancedOptions,
    QueryManagement,
    ServerSideAdTracking,
)
from bpkio_cli.core.app_context import AppContext


def create_ad_insertion_service_command():
    # COMMAND: CREATE
    @bic_res_cmd.command(
        help="Create a (simple) Ad Insertion service", takes_id_arg=False
    )
    @click.pass_obj
    def create(obj: AppContext):
        create_ad_insertion_service_via_prompts(obj)

    return create


def create_ad_insertion_service_via_prompts(obj: AppContext):
    all_sources = obj.api.sources.list()

    # Ask for the source
    sources = [
        s for s in all_sources if s.type in (SourceType.LIVE, SourceType.ASSET_CATALOG)
    ]
    sources = sorted(sources, key=lambda s: s.id, reverse=True)
    sources = obj.cache.sort_resources_by_most_recently_accessed(sources)
    choices = [
        dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]") for s in sources
    ]
    source_id = prompt.fuzzy(
        message="Source",
        choices=choices,
    )
    selected_source = next(s for s in sources if s.id == source_id)
    source_type = selected_source.type
    source_url_params = []

    # Then ask for the ad server
    ad_sources = [s for s in all_sources if s.type == SourceType.AD_SERVER]
    ad_sources = sorted(ad_sources, key=lambda s: s.id, reverse=True)
    ad_sources = obj.cache.sort_resources_by_most_recently_accessed(ad_sources)
    choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in ad_sources]
    ad_source_id = prompt.fuzzy(
        message="Ad Server",
        choices=choices,
    )

    # Ask for the type of ad insertion (optionally)
    if source_type in (SourceType.ASSET, SourceType.ASSET_CATALOG):
        insertion_types = ["vodAdInsertion"]
    else:
        choices = [
            dict(value="liveAdPreRoll", name="Live Pre-Roll"),
            dict(value="liveAdReplacement", name="Live Ad Replacement"),
        ]
        insertion_types = prompt.select(
            message="Ad Insertion Type",
            choices=choices,
            multiselect=True,
            long_instruction="More than one can be selected, with space key or ctrl+r",
        )

    # Extract the query params from the live source
    if source_type == SourceType.LIVE:
        live_source_url = urlparse(selected_source.url)
        source_url_params = list(parse_qs(live_source_url.query).keys())
        click.echo(f"Query parameters to forward to origin: {source_url_params}")

    # Specific options
    max_duration = None
    if "liveAdPreRoll" in insertion_types:
        # Ask for the duration
        max_duration = prompt.text(
            message="Max duration (in seconds) for pre-roll",
            default="60",
            validate=lambda result: result.isdigit(),
            invalid_message="The duration must be a number.",
        )

    if "liveAdReplacement" in insertion_types:  # Then ask for the gap filler
        slate_sources = [s for s in all_sources if s.type == SourceType.SLATE]
        slate_sources = sorted(slate_sources, key=lambda s: s.id, reverse=True)
        slate_sources = obj.cache.sort_resources_by_most_recently_accessed(
            slate_sources
        )
        choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in slate_sources]
        choices = [dict(value=None, name="-- No gap filler --")] + choices
        slate_source_id = prompt.fuzzy(
            message="Gap Filler (for ad replacement)",
            choices=choices,
        )

    # SSAT?
    with_ssat = prompt.confirm(message="Enable SSAT?")

    # Ask for transcoding profile
    profiles = obj.api.transcoding_profiles.list()
    profiles = obj.cache.sort_resources_by_most_recently_accessed(profiles)
    choices = [dict(value=s.id, name=f"({s.id})  {s.name}") for s in profiles]
    # ... add a "none" one
    choices = [dict(value=None, name="-- No transcoding --")] + choices
    transcoding_profile_id = prompt.fuzzy(
        message="Transcoding Profile",
        choices=choices,
    )

    # Ask for other options
    with_transcoding = transcoding_profile_id is not None

    name = prompt.text(
        message="Name for the service",
        validate=lambda result: len(result) > 0,
        invalid_message="The name cannot be empty.",
        default=f"[bic:svc.create] {selected_source.name}"
    )

    # Create the service object
    service = AdInsertionServiceIn(
        name=name,
        source=dict(id=source_id),
        enableAdTranscoding=with_transcoding,
        serverSideAdTracking=ServerSideAdTracking(enable=with_ssat),
        advancedOptions=None,
    )

    if source_url_params:
        service.advancedOptions = AdvancedOptions(
            queryManagement=QueryManagement(
                forwardInOriginRequest=source_url_params,
                addToHLSMediaPlaylistURI=[],
                addToMediaSegmentURI=[],
            ),
        )

    for ad_insertion_type in insertion_types:
        ad_insertion = dict(adServer=dict(id=ad_source_id))
        if ad_insertion_type == "liveAdPreRoll" and max_duration is not None:
            ad_insertion["maxDuration"] = int(max_duration)
        if ad_insertion_type == "liveAdReplacement" and slate_source_id is not None:
            ad_insertion["gapFiller"] = dict(id=slate_source_id)

        setattr(
            service,
            ad_insertion_type,
            ad_insertion,
        )

    if with_transcoding:
        # setattr(service, "transcodingProfile", dict(id=transcoding_profile_id))
        service.transcodingProfile = dict(id=transcoding_profile_id)

    service_out = obj.api.services.ad_insertion.create(service)

    obj.response_handler.treat_single_resource(service_out)
