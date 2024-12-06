import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.utils.prompt as prompt
import click
from bpkio_api.models.Services import ServiceType
from bpkio_cli.commands.creators.ad_insertion import \
    create_ad_insertion_service_via_prompts
from bpkio_cli.commands.creators.virtual_channel import \
    create_virtual_channel_service_with_prompts
from bpkio_cli.core.app_context import AppContext
from InquirerPy.base.control import Choice


def create_service_command():

    @bic_res_cmd.command(
        takes_id_arg=True,
        help="Create a Service from other resources. "
        "The CLI will prompt you for the information it needs.",
    )
    @click.pass_obj
    def create(obj: AppContext):
        service_type = prompt.select(
            message="What type of service do you want to create?",
            choices=[
                Choice(ServiceType.AD_INSERTION, name="Dynamic Ad Insertion"),
                Choice(ServiceType.VIRTUAL_CHANNEL, name="Virtual Channel"),
            ],
            multiselect=False,
        )

        if service_type == ServiceType.AD_INSERTION:
            create_ad_insertion_service_via_prompts(obj)
        if service_type == ServiceType.VIRTUAL_CHANNEL:
            create_virtual_channel_service_with_prompts(obj)

    return create
