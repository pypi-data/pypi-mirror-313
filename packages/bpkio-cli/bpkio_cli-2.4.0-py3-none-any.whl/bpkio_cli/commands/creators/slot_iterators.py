import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.models import ContentReplacementService, VirtualChannelService
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.utils.progressbar import widgets_slots
from progressbar import ProgressBar


def get_service_endpoint(context: AppContext, id: int):
    service = context.api.services.retrieve(id)

    if isinstance(service, VirtualChannelService):
        return context.api.services.virtual_channel
    if isinstance(service, ContentReplacementService):
        return context.api.services.content_replacement
    else:
        raise BroadpeakIoCliError("No slots on this type of service")


def replicate_slots_command():
    # COMMAND: REPLICATE
    @cloup.command(help="Copy slots into another service")
    @click.option(
        "--into",
        "target_id",
        help="The ID of the Service into which slots are to be copied",
        required=True,
        type=int,
    )
    @bic_options.slots("now", "24 hours")
    @click.pass_obj
    def replicate(obj: AppContext, target_id, start, end, categories, **kwargs):
        service_id = obj.resource_chain.last_key()
        api = get_service_endpoint(obj, service_id)
        replicate_slots(api, service_id, target_id, start, end, categories)

    return replicate


def replicate_slots(api, source_id, target_id, start, end, categories):
    source_service = api.retrieve(source_id)
    target_service = api.retrieve(target_id)

    source_slots = api.slots.list(
        service_id=source_service.id,
        from_time=start,
        to_time=end,
        categories=categories,
    )

    added = 0
    failed_messages = []

    with ProgressBar(
        widgets=widgets_slots("Copying slots"),
        max_value=len(source_slots),
        redirect_stdout=True,
    ) as bar:
        for i, source_slot in enumerate(source_slots):
            # we need to remove duration, as the API refuses to have both end time and duration
            source_slot.duration = None
            try:
                api.slots.create(target_service.id, source_slot)
                added += 1
            except Exception as e:
                failed_messages.append(e)
            bar.update(i, success=added, error=len(failed_messages))

    click.secho(f"Copied {added} slots", fg="green")
    if failed_messages:
        click.secho(f"Failed to add {len(failed_messages)} slots", fg="red")
        click.secho("- " + "\n- ".join(map(str, failed_messages)), fg="red")


# ---


def clear_slots_command():
    # COMMAND: CLEAR
    @cloup.command(help="Remove all slots in the service")
    @click.confirmation_option(prompt="Are you sure you want to delete all slots?")
    @bic_options.slots("now", "24 hours", allcats=True)
    @click.pass_obj
    def clear(obj: AppContext, start, end, categories, all_categories, **kwargs):
        service_id = obj.resource_chain.last_key()
        api = get_service_endpoint(obj, service_id)
        clear_slots(api, service_id, start, end, categories)

    return clear


def clear_slots(api, service_id, start, end=None, categories=[]):
    slots = api.slots.list(service_id, start, end, categories)

    deleted = 0
    failed_messages = []

    with ProgressBar(
        widgets=widgets_slots("Deleting slots"),
        max_value=len(slots),
        redirect_stdout=True,
    ) as bar:
        for i, slot in enumerate(slots):
            try:
                api.slots.delete(service_id, slot.id)
                deleted += 1
            except Exception as e:
                failed_messages.append(e)
            bar.update(i, success=deleted, error=len(failed_messages))

    if failed_messages:
        click.secho(f"Failed to delete {len(failed_messages)} slots", fg="red")
        click.secho("- " + "\n- ".join(map(str, failed_messages)), fg="red")
