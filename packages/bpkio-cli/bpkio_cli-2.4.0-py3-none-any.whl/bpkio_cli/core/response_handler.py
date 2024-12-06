import csv
import json as j
import re
from io import StringIO
from typing import List, Optional

import click
from bpkio_api.models import BaseResource
from bpkio_cli.core.resource_recorder import ResourceRecorder
from bpkio_cli.utils.arrays import pluck_and_cast_properties, sort_objects
from bpkio_cli.writers.breadcrumbs import display_tip
from bpkio_cli.writers.json_formatter import JSONFormatter
from bpkio_cli.writers.tables import display_table
from bpkio_cli.writers.urls import pretty_url
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console(stderr=True)


class ResponseHandler:
    def __init__(self, cache: Optional[ResourceRecorder] = None) -> None:
        self.cache = None
        if cache:
            self.cache = cache

    def treat_list_resources(
        self,
        resources: List,
        select_fields: Optional[List[str]] = None,
        sort_fields: Optional[List[str]] = [],
        format: Optional[str] = None,
        id_only: Optional[bool] = False,
        return_first: Optional[bool] = False,
    ):
        if not len(resources):
            return

        # Extract the select_fields
        if select_fields:
            select_fields = " ".join(select_fields)  # type: ignore
            select_fields = re.findall(r"\w[\w\.]*", select_fields)  # type: ignore
        else:
            select_fields = []

        # Sort the list
        if sort_fields and len(sort_fields):
            sort_by = " ".join(sort_fields)  # type: ignore
            sort_by = re.findall(r"\w[\w\.\:]*", sort_by)  # type: ignore
            sort_by = {
                i.split(":")[0]: i.split(":")[1] if len(i.split(":")) > 1 else "asc"
                for i in sort_by
            }
            # add sort fields to fields list if not already present
            for f in sort_by.keys():
                if f not in select_fields:
                    select_fields.append(f)

            resources = sort_objects(resources, sort_by=sort_by)

        if return_first:
            return self.treat_single_resource(resources[0], format, id_only)

        # Register the (transformed) list into cache
        if self.cache:
            self.cache.record(resources)

        if id_only:
            for r in resources:
                print(r.id)
            return

        # Output the JSON representation
        if format == "json":
            if isinstance(resources[0], BaseModel):
                resources = [j.loads(r.json(exclude_none=True)) for r in resources]

            colored_json = JSONFormatter().format(resources)
            click.echo(colored_json)
            return

        # Extract the select_fields
        if select_fields:
            select_fields = " ".join(select_fields)  # type: ignore
            select_fields = re.findall(r"\w[\w\.]*", select_fields)  # type: ignore

        data = pluck_and_cast_properties(resources, select_fields)

        if format == "csv":
            export_csv(data)
            return

        # Else print it as a table
        display_table(data)

    def treat_single_resource(
        self,
        resource: object,
        format: Optional[str] = None,
        id_only: Optional[bool] = False,
    ):
        # Record the resource
        if self.cache and hasattr(resource, "id"):
            self.cache.record(resource)
            display_tip(
                f"Context switched for {resource.__class__.__name__} resource to id '{resource.id}'"
            )

        if id_only:
            click.echo(resource.id)
            return resource

        if format == "json" and isinstance(resource, BaseModel):
            data = j.loads(resource.json(exclude_none=False))
            colored_json = JSONFormatter().format(data)
            click.echo(colored_json)

            return resource

        elif not isinstance(resource, BaseResource):
            colored_json = JSONFormatter().format(resource)
            click.echo(colored_json)

            return resource

        else:
            rows = []

            # Identifier
            header = "{} {}".format(
                click.style(resource.__class__.__name__, fg="white", dim=True),
                click.style(resource.id, fg="white"),
            )
            # rows.append(header)

            # Name and description
            title = []
            title.append(click.style(resource.name, fg="white", bold=True))
            if hasattr(resource, "description") and resource.description is not None:
                title.append(click.style(resource.description, fg="white"))
            rows.append("\n".join(title))

            # URL
            if hasattr(resource, "url"):
                url = (
                    resource.make_full_url()
                    if hasattr(resource, "make_full_url")
                    else resource.url
                )

                formatted_url = pretty_url(
                    url, path_highlight=getattr(resource, "assetSample", None)
                )

                rows.append(formatted_url)

            console.print(
                Panel(
                    Text.from_ansi("\n".join(rows)),
                    title=Text.from_ansi(header),
                    title_align="left",
                    expand=False,
                    highlight=True,
                )
            )

            # print it to pass in pipes
            click.echo(resource.id)

    @staticmethod
    def treat_simple_list(data: list):
        display_table(data)
        return


def export_csv(data):
    # Find all unique keys
    keys = list()
    for obj in data:
        for k in obj.keys():
            if k not in keys:
                keys.append(k)

    # Write to CSV
    output = StringIO()
    dict_writer = csv.DictWriter(output, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)

    # Get CSV data as a string
    csv_str = output.getvalue()
    print(csv_str)

    # Close the StringIO object
    output.close()


def save_resource(resource):
    if not isinstance(resource, BaseResource):
        raise NotImplementedError(
            f"Resource of type {resource.__class__.__name__} cannot be saved"
        )

    filename = f"{resource.__class__.__name__}_{resource.id}"

    # Convert to JSON
    resource = j.loads(resource.json(exclude_none=False))

    save_json(resource, filename, resource.__class__.__name__)


def save_json(payload, filename, resource_type):
    filename = f"{filename}.json"

    with open(filename, "w") as f:
        j.dump(payload, f, indent=4)
    click.secho(f"{resource_type} saved to {filename}", fg="green")
