import click
from bpkio_api.models.Sources import SourceStatusCheckResult


def display_source_status(obj, result: SourceStatusCheckResult, as_json: bool = False):
    if as_json:
        obj.response_handler.treat_single_resource(resource=result.dict())
    else:
        if result.sourceStatus == "WARN":
            click.echo("Status: ", nl=False)
            click.secho(result.sourceStatus, fg="yellow")
            for warning in result.warnings:
                click.secho("- " + warning["description"], fg="yellow")

        if result.sourceStatus == "KO":
            click.echo("Status: ", nl=False)
            click.secho(result.sourceStatus, fg="red")
            for error in result.errors:
                click.secho("- " + error["description"], fg="red")

        if result.sourceStatus == "OK":
            click.echo("Status: ", nl=False)
            click.secho(result.sourceStatus, fg="green")
