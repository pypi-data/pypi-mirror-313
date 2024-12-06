import functools

import click


def extra_tenant_option(required=False):
    def decorator(fn):
        @click.option(
            "--tenant",
            type=int,
            required=False,
            callback=validate_target_tenant_id if required else None,
            help="[ADMIN] ID of the tenant",
        )
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper
    return decorator


def validate_target_tenant_id(ctx, param, value):
    # determine target tenant
    if value is None:
        if ctx.obj.tenant.id == 1:
            raise click.BadParameter(
                "You must specify a target tenant ID when manipulating a profile"
            )
        value = ctx.obj.tenant.id

    # click.echo(f"Target tenant is tenant {value}")
    return value
