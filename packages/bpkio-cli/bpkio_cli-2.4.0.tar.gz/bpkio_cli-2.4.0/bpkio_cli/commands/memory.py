import click
import cloup
from bpkio_cli.core.app_context import AppContext


@cloup.group(aliases=["mem"], help="App resource registry comands")
@click.pass_obj
def memory(obj: AppContext):
    pass


@memory.command(help="Clear the app resource register")
@click.pass_obj
def clear(obj: AppContext):
    obj.cache.clear()


@memory.command(help="Check what is stored in the app's resource register")
@click.pass_obj
def read(obj: AppContext):
    click.secho("Last resources accessed", fg="yellow")
    for v in obj.cache.list_resources():
        click.secho(" · " + v.__class__.__name__ + " ", fg="green", nl=False)
        click.secho(v.summary if hasattr(v, "summary") else v)

    click.secho("Last lists retrieved", fg="yellow")
    for k, lst in obj.cache.list_lists().items():
        try:
            list_ids = [item.id for item in lst]
            click.secho(" · " + k + " ", fg="green", nl=False)
            click.secho(list_ids)
        except Exception:
            pass

    click.secho("Last Metadata", fg="yellow")
    for k, metadata in obj.cache.list_metadata().items():
        try:
            click.secho(" · " + k + " ", fg="green", nl=False)
            click.secho(metadata)
        except Exception:
            pass


@memory.command(help="Clear the cache for a single resource")
@cloup.argument("id", help="The id of the resource", type=int)
@click.pass_obj
def forget(obj: AppContext, id: int):
    obj.cache.remove_by_id(id)
