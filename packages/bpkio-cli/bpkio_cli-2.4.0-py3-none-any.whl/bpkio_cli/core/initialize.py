import os
from importlib.metadata import version

import click
from bpkio_api import BroadpeakIoApi
from bpkio_api.credential_provider import TenantProfileProvider
from bpkio_api.exceptions import InvalidTenantError, NoTenantSectionError
from bpkio_api.models import BaseResource
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from media_muncher.handlers.generic import ContentHandler

cli_agent = f"bpkio-cli/{version('bpkio-cli')}"


def initialize(
    requires_api: bool, tenant: str | int | None = None, use_cache: bool = True
) -> AppContext:
    """Function that initialises the CLI

    If a tenant label or ID is provided, the CLI will be initialised for that tenant.
    Otherwise, the CLI will be initialised with the last tenant used (and stored in
    a `.tenant` file).

    Successful initialisation requires that there is a profile in ~/.bpkio/tenants
    for that tenant.

    Args:
        tenant (str | int): Name of the CLI profile or ID of the tenant

    Raises:
        click.Abort: if no tenant profile could be found in the ~/.bpkio/tenants file

    Returns:
        AppContext: The config for the app
    """
    tp = TenantProfileProvider()

    # No specific tenant provided, see if there is one defined for the current directory
    if not tenant:
        tenant = tp.get_tenant_label_from_working_directory()
    else:
        tenant = str(tenant)

    # Define a file to store a recording of actions
    session_file = None
    session_sentinel = os.path.expanduser("~/.bpkio/cli_session")
    if os.path.exists(session_sentinel):
        # open it and extract the path to the session file.
        with open(session_sentinel, "r") as f:
            session_file = f.read()

    # Append to the content handler client string (sent as header)
    ContentHandler.api_client = cli_agent + " " + ContentHandler.api_client

    # Set verify_ssl for the content handlers as well
    ContentHandler.verify_ssl = CONFIG.get("verify-ssl", "bool_or_str")

    try:
        api = BroadpeakIoApi(
            tenant=tenant,
            use_cache=use_cache,
            session_file=session_file,
            user_agent=cli_agent,
            verify_ssl=CONFIG.get("verify-ssl", "bool_or_str"),
            api_client=f"bpkio-cli/{version('bpkio-cli')}",
        )
        app_context = AppContext(api=api, tenant_provider=TenantProfileProvider())

        if CONFIG.get("verbose", int) > 0:
            full_tenant = api.get_self_tenant()
            app_context.tenant = full_tenant
        else:
            app_context.tenant = BaseResource(id=api.get_tenant_id())

        # Check size of the session recorder, in case it was left on
        # from a previous run.
        if api.session_recorder.is_active():
            click.secho(
                "⚠️  WARNING: Active recording session (with %s records)"
                % api.session_recorder.size(),
                fg="magenta",
                err=True,
            )

    except NoTenantSectionError as e:
        if requires_api:
            raise BroadpeakIoCliError(f"This command requires a valid tenant to be specified: {e}")
        else:
            app_context = AppContext(api=None, tenant_provider=TenantProfileProvider())            

    except InvalidTenantError:
        if requires_api:
            raise BroadpeakIoCliError("This command requires a valid tenant to be configured. Try `bic init` to configure a tenant.")
        else:
            app_context = AppContext(api=None, tenant_provider=TenantProfileProvider())

    return app_context
