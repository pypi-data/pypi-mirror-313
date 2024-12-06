import click

from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.writers.logo import show_logo


# Command: HELLO
@click.command(hidden=True)
@click.pass_obj
def hello(obj: AppContext):
    """Validate access to the API and display tenant information"""

    if CONFIG.get("verbose", int) > 1:
        show_logo()

    tenant = obj.api.get_self_tenant()
    candidate_users = obj.api.users.list()
    candidate_users.sort(key=lambda u: u.creationDate)
    user = candidate_users[0]

    click.echo(f'You are working with tenant "{tenant.name}"  [id: {tenant.id}]')
    click.echo(
        f'The first user in that account is "{user.firstName}"  [email: {user.email}]'
    )
    if not obj.api.uses_default_fqdn():
        click.echo(
            f"This tenant is using a non-default API entrypoint at {obj.api._fqdn}"
        )
