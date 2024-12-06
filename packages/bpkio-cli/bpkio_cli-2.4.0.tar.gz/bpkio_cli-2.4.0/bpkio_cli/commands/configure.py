import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.commands.tenant_profiles import add, tenants
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.response_handler import ResponseHandler
from bpkio_cli.writers.players import StreamPlayer


# Command: INIT
# To be attached to the root group
@cloup.command(help="Initialize the tool, and create a first tenant profile")
@click.pass_context
def init(ctx):

    if not ctx.obj.tenant_provider.has_default_tenant():
        ctx.invoke(add)

    click.secho("All done!  You're ready to go now", fg="yellow")


# Group: CONFIG
@cloup.group(
    aliases=["config", "cfg"],
    help="Configure how the CLI works",
    show_subcommand_aliases=True,
)  # type: ignore
@click.pass_obj
def configure(obj):
    pass


# Command: SET
@configure.command(help="Set a configuration option")
@click.argument("key", required=True)
@click.argument("value", required=True)
def set(key, value):
    if "." in key:
        key_parts = key.split(".")
        section = key_parts[0]
        key = ".".join(key_parts[1:])
        CONFIG.set_config(key, value, section=section)
    else:
        CONFIG.set_config(key, value)


# Command: EDIT
@configure.command(help="Edit the config file")
def edit():
    config_file = CONFIG.config_path
    click.edit(filename=str(config_file), editor=CONFIG.get("editor"))


# =========

# Sub-group: TENANTS
configure.add_command(tenants)

# =========


# Sub-Group: PLAYERS
@configure.group(
    help="Management of player configurations",
    aliases=["player", "pl"],
)
@click.pass_obj
def players(obj):
    pass


# Command: LIST
@players.command(help="List the players already configured", aliases=["ls"])
@bic_options.output_formats
@click.option(
    "-s",
    "--sort",
    "sort_fields",
    cls=OptionEatAll,
    type=tuple,
    help="List of fields used to sort the list. Append ':desc' to sort in descending order",
)
@click.option(
    "--labels",
    "labels_only",
    is_flag=True,
    type=bool,
    default=False,
    help="Return the labels only, 1 per line. This can be useful for piping to other tools",
)
def list(sort_fields, labels_only, list_format):
    pl = StreamPlayer()
    ppl = pl.available_player_templates()
    if labels_only:
        ppl = [p for p in ppl.keys()]
        click.echo("\n".join(ppl))
    else:
        ppl = [v for k, v in ppl.items()]
        ResponseHandler().treat_list_resources(
            resources=ppl,
            # select_fields=["label", "id", "fqdn"],
            sort_fields=sort_fields,
            format=list_format,
        )


# =========
