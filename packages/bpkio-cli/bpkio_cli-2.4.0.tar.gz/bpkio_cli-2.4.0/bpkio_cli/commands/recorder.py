import bpkio_cli.core.session_recorder as recorder
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder


# Group: RECORDER
@cloup.group(
    help="Use a Session Recorder to record and replay commands",
)
@click.pass_context
def record(ctx):
    pass


@record.command(help="Start a recording")
@cloup.argument(
    "session_name",
    help="The name of the session to record",
    required=False,
)
def start(session_name):
    session_file_path = recorder.make_session_file(session_name)

    click.secho("» Recording session started in " + session_file_path, fg="green")


@record.command(help="Stop a recording")
def stop():
    try:
        session_file_path = recorder.get_session_file()
    except Exception:
        click.secho("» No active recording session", fg="red")
        return

    remove = prompt.confirm(
        message=f"Would you like to delete the session file at {session_file_path}?"
    )
    if remove:
        try:
            recorder.destroy_session_file()
            click.secho("» Session file deleted", fg="green")
        except FileNotFoundError:
            click.secho("» The session file did not exist", fg="red")

    recorder.remove_sentinel()
    click.secho("» Recording session stopped", fg="green")


@record.command(help="Export a session")
@click.option(
    "-f",
    "--format",
    "format",
    help="The format of the export",
    default="text",
    type=click.Choice(["text", "markdown", "postman", "har", "curl"]),
)
@click.option(
    "--safe/--no-safe",
    help="Remove sensitive information from the session",
    default=True,
)
@click.option(
    "--with-response/--without-response",
    "with_response",
    help="Include the response in the export",
    default=False,
)
@click.option(
    "--with-list/--without-list",
    "with_lists",
    help="Include calls returning lists (only if --with-get is also set)",
    default=False,
)
@click.option(
    "--with-get/--without-get",
    "with_gets",
    help="Include GET calls",
    default=True,
)
@click.option(
    "--compact/--readable",
    "compact",
    default=False,
    help="Prefers a compact or more readable output (for formats supporting it)",
)
def export(format, safe: bool, with_response, with_lists, with_gets, compact):
    options = dict(
        format=format,
        remove_secrets=safe,
        include_response=with_response,
        include_list=with_lists,
        include_get=with_gets,
        compact=compact,
    )

    session_file_path = recorder.get_session_file()

    SessionRecorder(session_file_path).export(options)
