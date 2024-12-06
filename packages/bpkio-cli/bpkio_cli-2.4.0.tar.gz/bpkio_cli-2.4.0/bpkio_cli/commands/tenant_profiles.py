# Sub-Group: TENANTS
import json
import re
import uuid

import click
import cloup
from bpkio_api.api import BroadpeakIoApi
from bpkio_api.credential_provider import TenantProfile, TenantProfileProvider
from bpkio_api.defaults import DEFAULT_FQDN
from rich.console import Console
from rich.live import Live
from rich.table import Table

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.commands.hello import hello
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.response_handler import ResponseHandler
from bpkio_cli.utils import prompt
from bpkio_cli.utils.onepassword import (
    get_detailed_item,
    is_op_cli_installed,
    is_op_secret,
    list_all_candidate_items,
    store_api_key_in_op,
)
from bpkio_cli.writers.breadcrumbs import display_ok, display_tip

console = Console()


@bic_res_cmd.group(
    aliases=["tenant", "tnt"],
    cls=bic_res_cmd.ResourceGroup,
    help="Define CLI credential profiles to be able to easily switch tenant",
    resource_type=TenantProfile,
)
@cloup.argument("tenant_label", metavar="<tenant-label>")
@click.pass_obj
def tenants(obj: AppContext, tenant_label):
    if tenant_label and tenant_label != bic_res_cmd.ARG_TO_IGNORE:
        if tenant_label == "$":
            tenant_label = obj.tenant_provider.get_tenant_label_from_working_directory()
        if not obj.tenant_provider.has_tenant_label(tenant_label):
            raise click.ClickException(f"Tenant '{tenant_label}' not found")
        tenant = obj.tenant_provider.get_tenant_profile(tenant_label=tenant_label)

        obj.resource_chain.overwrite_last(tenant_label, tenant)


def resolve_platform(ctx, param, value):
    return TenantProfileProvider.resolve_platform(value)


# Command: LIST
@tenants.command(
    help="List the tenants configured",
    aliases=["ls"],
    takes_id_arg=False,
    is_default=True,
)
@bic_options.output_formats
@click.option(
    "-s",
    "--sort",
    "sort_fields",
    cls=OptionEatAll,
    type=tuple,
    help="List of fields used to sort the list. Append ':desc' to sort in descending order",
    default=("label",),
)
@click.option(
    "-p",
    "--platform",
    type=str,
    help="Filter the list by platform (eg. 'prod', 'poc1')",
    default=None,
    callback=resolve_platform,
)
@click.option(
    "--labels",
    "labels_only",
    is_flag=True,
    type=bool,
    default=False,
    help="Return the labels only, 1 per line. This can be useful for piping to other tools",
)
@click.pass_obj
def list(obj: AppContext, sort_fields, labels_only, list_format, platform):
    tenants = obj.tenant_provider.list_tenants()

    if platform:
        if platform == "prod":
            platform = "api."
        if platform == "staging":
            platform = "test."
        tenants = [t for t in tenants if platform in t.fqdn]

    if labels_only:
        tenants = [t.label for t in tenants]
        click.echo("\n".join(tenants))
    else:
        ResponseHandler().treat_list_resources(
            resources=tenants,
            select_fields=["label", "id", "fqdn"],
            sort_fields=sort_fields,
            format=list_format,
        )


# Command: SWITCH
@tenants.command(
    help="Switch the tenant used for subsequent invocations", takes_id_arg=False
)
@click.argument("tenant", required=False, metavar="<tenant-label>")
@click.pass_context
def switch(ctx, tenant):
    if not tenant:
        cp = ctx.obj.tenant_provider
        tenant_list = cp.list_tenants()
        tenant_list = sorted(tenant_list, key=lambda t: t.label)
        choices = [
            dict(value=t.label, name=f"{t.label} ({t.id})  -  {t.fqdn}")
            for t in tenant_list
        ]

        tenant = prompt.fuzzy(message="Select a tenant", choices=choices)

    # Reinitialize the app context
    ctx.obj = initialize(tenant=tenant, requires_api=True)

    # Write it to the .tenant file
    ctx.obj.tenant_provider.store_tenant_label_in_working_directory(tenant)

    # show tenant info to the user for validation
    ctx.invoke(hello)


# Command: ADD
@tenants.command(help="Store credentials for a new tenant", takes_id_arg=False)
@click.argument("label", required=False)
@click.pass_context
def add(ctx, label):
    cp = ctx.obj.tenant_provider
    verify_ssl = CONFIG.get("verify-ssl", "bool_or_str")

    api_key = prompt.secret(
        message="API Key for the Tenant",
        long_instruction="Get your API key from the broadpeak.io webapp",
        validate=lambda candidate: BroadpeakIoApi.is_valid_api_key_format(candidate),
        invalid_message="Invalid API Key",
    )

    # Detect the FQDN from the API key
    fqdn = None
    key_payload = BroadpeakIoApi._parse_api_key(api_key)
    if domain := key_payload.get("domain"):
        if domain == "b":
            fqdn = "broadpeak.io"
        if domain == "r":
            fqdn = "ridgeline.fr"

        env = key_payload.get("env")
        fqdn = f"api{env}.{fqdn}"

    fqdn_for_prompt = DEFAULT_FQDN
    # check it
    if not BroadpeakIoApi.is_correct_entrypoint(fqdn, api_key, verify_ssl):
        fqdn_for_prompt = fqdn
        fqdn = None

    if not fqdn:
        fqdn = prompt.text(
            message="Domain name for the API endpoints",
            default=fqdn_for_prompt,
            long_instruction="You can also paste the URL to the webapp, if you don't know the API endpoint",
            validate=lambda url: BroadpeakIoApi.is_correct_entrypoint(
                url, api_key, verify_ssl=verify_ssl
            ),
            filter=lambda url: BroadpeakIoApi.normalise_fqdn(url),
            invalid_message=(
                "This URL does not appear to be a broadpeak.io application, "
                "or your API key does not give you access to it"
            ),
        )

    # Test the API key by initialising the API with it
    bpk_api = BroadpeakIoApi(api_key=api_key, fqdn=fqdn, verify_ssl=verify_ssl)

    # Parse the API
    tenant = bpk_api.get_self_tenant()
    tenant_id = tenant.id

    default_name = label or tenant.name
    default_name = re.sub(r"[^a-zA-Z0-9\-_\@]", "_", default_name)
    # If there is no default profile yet, suggest that one instead
    if not cp.has_default_tenant():
        default_name = "default"

    key = prompt.text(
        message="Profile label",
        default=default_name,
        long_instruction="This label will be used to identify the tenant in the future. Make it short, easy and memorable.",
        validate=lambda s: bool(re.match(r"^[a-zA-Z0-9_\-\@]*$", s)),
        invalid_message="Please only use alphanumerical characters",
    )

    # Create a dict
    config = {"api_key": api_key, "id": tenant.id}

    if fqdn != DEFAULT_FQDN:
        config["fqdn"] = fqdn

    if is_op_cli_installed():
        use_1password = prompt.confirm(
            message="1Password detected. Do you want to store the API key in 1Password?",
            default=True,
        )
        if use_1password:
            # Store the API key in 1Password
            secret = store_api_key_in_op(
                api_key=api_key,
                tenant_label=key,
                tenant_name=tenant.name,
                tenant_id=tenant.id,
                fqdn=fqdn,
                expiration=key_payload.get("exp"),
                valid_from=key_payload.get("iat"),
            )
            config["api_key"] = secret

    cp.add_tenant(key, config)

    display_ok(
        f'A profile named "{key}" for tenant {tenant_id} has been added to {cp.inifile}'
    )

    if key != "default":
        display_tip(
            f"You can now simply use `bic --tenant {key} COMMAND` to work within that tenant's account"
        )
    else:
        display_tip(
            "You can now simply use `bic COMMAND` to work within that tenant's account"
        )

    do_switch = prompt.confirm(
        message="Do you want to switch to this tenant now?", default=True
    )

    if do_switch:
        ctx.invoke(switch, tenant=key)


# Command: IMPORT
@tenants.command(
    name="import", help="Import tenant credentials from 1Password", takes_id_arg=False
)
@click.pass_obj
def import_from_1password(obj: AppContext):
    cp = obj.tenant_provider
    if not is_op_cli_installed():
        raise click.ClickException("1Password CLI is not installed")

    candidate_items = list_all_candidate_items()
    selected_item = prompt.fuzzy(
        message="Select an item to import",
        choices=[
            prompt.Choice(name=c["title"], value=c)
            for c in sorted(candidate_items, key=lambda t: t["updated_at"])
        ],
    )

    detailed_item = get_detailed_item(
        selected_item["id"],
        account_uuid=selected_item["vault"]["account_uuid"],
        vault_id=selected_item["vault"]["id"],
    )

    try:
        label = detailed_item["title"].replace(" ", "")
        api_key = (
            f"op://{detailed_item['vault']['id']}/{detailed_item['id']}/credential"
        )
        # get the field with name=id
        tenant_id = next(
            (f["value"] for f in detailed_item["fields"] if f["label"] == "id"), None
        )
        fqdn = next(
            (f["value"] for f in detailed_item["fields"] if f["label"] == "platform"),
            None,
        )

        entry = {
            "api_key": api_key,
            "id": tenant_id,
            "fqdn": fqdn,
        }

        # TODO - check whether the label already exists, and offer to overwrite or change the label
        cp.add_tenant(label, entry)

        display_ok(f"Tenant {label} has been imported from 1Password")

    except Exception:
        raise BroadpeakIoCliError(
            f"Failed to import tenant. The information in this 1Password entry does not match expectations"
        )


# Command: INFO
@tenants.command(help="Show information about a tenant", is_default=True)
@click.pass_obj
def info(obj: AppContext):
    tenant = obj.current_resource

    tb = Table(show_header=False)

    for k, v in dict(tenant).items():
        if k != "api_key":
            tb.add_row(k, str(v))

    try:
        bpk_api = BroadpeakIoApi(
            api_key=tenant.api_key, fqdn=tenant.fqdn, verify_ssl=False
        )
        full_tenant = bpk_api.get_self_tenant()
        if full_tenant.state == "enabled":
            tb.add_row("state", f"[green]{full_tenant.state}")
        else:
            tb.add_row("state", f"[yellow]{full_tenant.state}")
    except Exception as e:
        tb.add_row("state", f"[red]{e}")

    console.print(tb)


# Command: EDIT
@tenants.command(help="Edit the tenant credential file manually", takes_id_arg=False)
def edit():
    cp = TenantProfileProvider()

    click.edit(filename=str(cp.inifile), editor=CONFIG.get("editor"))


# Command: PASSWORD / API KEY
@tenants.group(help="Manage the API key for the current tenant", aliases=["password"])
def apikey():
    pass


@apikey.command(name="get", help="Retrieve the API key for the current tenant")
@click.pass_obj
def get_apikey(obj: AppContext):
    tenant = obj.current_resource
    click.echo(tenant.api_key)


@apikey.command(
    name="change", aliases=["set"], help="Change the API key for the current tenant"
)
@click.pass_obj
def change_apikey(obj: AppContext):
    verify_ssl = CONFIG.get("verify-ssl", "bool_or_str")

    tenant: TenantProfile = obj.current_resource

    if tenant.credential_source == "1Password":
        raise BroadpeakIoCliError(
            "This tenant is managed by 1Password. Please change the API key in 1Password instead."
        )

    new_api_key = prompt.secret(
        message="New API Key",
        validate=lambda key: BroadpeakIoApi.is_correct_entrypoint(
            tenant.fqdn, key, verify_ssl=verify_ssl
        ),
        invalid_message="Invalid API Key for this tenant or platform",
    )

    obj.tenant_provider.replace_tenant_api_key(key=tenant.label, api_key=new_api_key)


# Command: POSTMAN
@tenants.command(help="Export as Postman environment")
@click.pass_obj
def postman(obj: AppContext):
    tenant = obj.current_resource

    keys = [
        {
            "key": "API_TOKEN",
            "value": tenant.api_key,
            "type": "secret",
            "enabled": True,
        },
        {
            "key": "API_ROOT",
            "value": f"{tenant.fqdn}/v1",
            "type": "default",
            "enabled": True,
        },
        {
            "key": "API_FQDN",
            "value": tenant.fqdn,
            "type": "default",
            "enabled": True,
        },
        {
            "key": "TENANT_ID",
            "value": tenant.id,
            "type": "default",
            "enabled": True,
        },
    ]

    env = dict(
        id=str(uuid.uuid4()), name=f"bpk.io tenant - {tenant.label}", values=keys
    )

    with open(f"{tenant.label}.postman_environment.json", "w") as f:
        json.dump(env, f, indent=4)

    display_ok(f"Environment file saved to {tenant.label}.postman_environment.json")


# Command: CHECK
@tenants.command(
    help="Check connectivity to tenants, and account status", takes_id_arg=False
)
@click.option(
    "-p",
    "--platform",
    type=str,
    help="Filter the list by platform (eg. 'prod', 'poc1')",
    default=None,
    callback=resolve_platform,
)
@click.pass_obj
def check(obj: AppContext, platform):
    tenants = obj.tenant_provider.list_tenants()
    if platform:
        tenants = [t for t in tenants if platform in t.fqdn]

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("tenant", width=20)
    table.add_column("platform", width=30)
    table.add_column("status")

    with Live(table, refresh_per_second=4):
        for tenant in tenants:
            try:
                bpk_api = BroadpeakIoApi(
                    api_key=tenant.api_key, fqdn=tenant.fqdn, verify_ssl=False
                )
                t = bpk_api.get_self_tenant()
                if t.state == "enabled":
                    status = "[green]" + t.state
                else:
                    status = "[yellow]" + t.state
            except Exception as e:
                status = "[red]" + str(e)

            table.add_row(tenant.label, tenant.fqdn, status)


# Command: REMOVE
@tenants.command(help="Remove the tenant from local config")
@click.pass_obj
@click.confirmation_option(
    prompt="Are you sure you want to remove this tenant from your local config?"
)
def remove(obj: AppContext):
    tenant_label = obj.resource_chain.last_key()

    obj.tenant_provider.remove_tenant(tenant_label)
