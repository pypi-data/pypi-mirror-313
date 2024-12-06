import copy
import functools
from datetime import datetime, timezone
from typing import List

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import bpkio_cli.click_options as bic_options
import click
import cloup
from bpkio_api.helpers.recorder import SessionRecorder
from bpkio_api.helpers.times import to_local_tz, to_relative_time
from bpkio_cli.core.api_resource_helpers import (
    get_api_endpoint, retrieve_api_resource_from_chain)
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.resource_chain import ResourceChain
from bpkio_cli.core.resource_decorator import add_category_info
from bpkio_cli.utils.datetimes import seconds_to_timecode
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.colorizer import trim_or_pad
from tabulate import tabulate


def create_child_resource_group(
    name: str,
    resource_type: type,
    endpoint_path: List[str],
    aliases: List[str] = [],
    default_fields=["id", "name"],
    extra_commands=[],
):
    """Generates a group of CLI commands for CRUD-based sub-resources

    Args:
        name (str): The name of the command group
        endpoint_path (List[str]): List of the endpoint names that make the path of the
            corresponding api class (eg. ["sources", "virtual-channel", "slots"])
        aliases (List[str], optional): Aliases for the command name. Defaults to none.
        default_fields (list, optional): Base resource fields used for table displays.
            Defaults to ["id", "name", "type"].
        with_content_commands (bool | str): Defines whether the group contains commands
            for handling resource content (for sources and services)

    Returns:
        cloup.Group: The MultiCommand group with all its nested commands
    """
    sections = []

    resource_title = str.title(name.replace("-", " "))
    if len(endpoint_path) > 1:
        parent_resource_title = str.title(
            endpoint_path[-2].replace("-", " ").replace("_", " ")
        )
        resource_title = f"{parent_resource_title} {resource_title}"

    # === GROUP ===

    @bic_res_cmd.group(
        name=name,
        help=f"Commands for managing {resource_title}s",
        aliases=aliases,
        takes_id_arg=True,
        show_subcommand_aliases=True,
        resource_type=resource_type,
    )
    @cloup.argument(
        "id",
        metavar=f"<{name.replace('-', '_')}_id>",
        help=(
            f"The identifier of the {resource_title} to work with. "
            f"Leave empty for commands operating on a list of {resource_title}s."
        ),
    )
    @click.pass_context
    @SessionRecorder.do_not_record
    def resource_group(ctx, id):
        if id and id != bic_res_cmd.ARG_TO_IGNORE:
            resource = retrieve_api_resource_from_chain(id, endpoint_path=endpoint_path)
            display_resource_info(resource)

    # === CRUD Commands ===

    # --- LIST Command
    @bic_res_cmd.command(
        help=f"List all {resource_title}s",
        aliases=["ls"],
        takes_id_arg=False,
        is_default=True,
    )
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @bic_options.slots("1 hour ago", "in 1 hour")
    @click.option(
        "-sch",
        "--schedule",
        "as_columns",
        is_flag=True,
        default=False,
        help="Display as a schedule (one column per category)",
    )
    @click.pass_obj
    def list(
        obj: AppContext,
        list_format,
        select_fields,
        sort_fields,
        return_first,
        id_only,
        start,
        end,
        as_columns,
        categories,
        no_category,
        **kwargs,
    ):
        endpoint = get_api_endpoint(endpoint_path)

        click.secho(
            "Looking at a window of time between {} ({}) and {} ({})".format(
                to_local_tz(start),
                to_relative_time(start),
                to_local_tz(end),
                to_relative_time(end),
            ),
            fg="white",
            dim=True,
        )

        resources = endpoint.list(
            obj.resource_chain.last_key(),
            from_time=start,
            to_time=end,
            categories=categories,
        )

        # Add full categories if set
        add_category_info(resources)

        if not as_columns:
            obj.response_handler.treat_list_resources(
                resources,
                select_fields=select_fields,
                sort_fields=sort_fields,
                format=list_format,
                id_only=id_only,
                return_first=return_first,
            )
        else:
            group_slots_by_category(resources)

    # --- INFO Commmand
    @bic_res_cmd.command(help=f"Get a specific {resource_title} by ID")
    @bic_options.output_formats
    @click.pass_obj
    def info(obj: AppContext, list_format):
        resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
        add_category_info(resource)

        obj.response_handler.treat_single_resource(resource, format=list_format)

    # --- GET Commmand
    @bic_res_cmd.command(
        aliases=["retrieve", "json"],
        help=f"Get the JSON representation of a single {resource_title} "
        f"or list of {resource_title}s",
        is_default=True,
    )
    @click.pass_obj
    def get(obj: AppContext):
        try:
            resource = retrieve_api_resource_from_chain(endpoint_path=endpoint_path)
            add_category_info(resource)
            obj.response_handler.treat_single_resource(resource, format="json")
        except Exception:
            endpoint = get_api_endpoint(endpoint_path)
            resources = endpoint.list(obj.resource_chain.last_key())
            add_category_info(resources)
            obj.response_handler.treat_list_resources(resources, format="json")

    # --- SEARCH Command
    @bic_res_cmd.command(
        help=f"Retrieve a list of all {resource_title}s "
        "that match given terms in all or selected fields",
        takes_id_arg=False,
    )
    @bic_options.search
    @bic_options.list(default_fields=default_fields)
    @bic_options.output_formats
    @click.pass_obj
    def search(
        obj: AppContext,
        single_term,
        search_terms,
        search_fields,
        list_format,
        select_fields,
        sort_fields,
        id_only,
        return_first,
    ):
        search_def = bic_options.validate_search(
            single_term, search_terms, search_fields
        )

        endpoint = get_api_endpoint(endpoint_path)
        resources = endpoint.search(obj.resource_chain.last_key(), filters=search_def)
        add_category_info(resources)

        obj.response_handler.treat_list_resources(
            resources,
            select_fields=select_fields,
            sort_fields=sort_fields,
            format=list_format,
            id_only=id_only,
            return_first=return_first,
        )

    # --- DELETE Commmand
    @bic_res_cmd.command(
        aliases=["del"], help=f"Delete a specific {resource_title} by ID"
    )
    @click.confirmation_option(prompt="Are you sure you want to delete this resource?")
    @click.pass_context
    def delete(ctx):
        resource_chain: ResourceChain = click.get_current_context().obj.resource_chain
        id = resource_chain.last_key()
        parent_id = resource_chain.parent()

        endpoint = get_api_endpoint(endpoint_path)
        endpoint.delete(parent_id, id)

        click.secho(f"Resource {id} deleted", fg="green")

    sections.append(cloup.Section("CRUD commands", [get, info, list, search, delete]))

    # === EXTRA Commands
    # Go through extra commands and add them where relevant...

    sections.append(cloup.Section("Other commands", []))

    for new_command in extra_commands:
        inserted = False
        for section in sections:
            for k in section.commands.keys():
                if k == new_command.name:
                    # ... override an existing one ...
                    section.commands[k] = new_command
                    inserted = True
        if not inserted:
            # ... or add it to the last section
            if new_command.name in ["create", "update", "delete"]:
                for section in sections:
                    if section.title == "CRUD commands":
                        section.add_command(new_command)
                        break
            else:
                sections[-1].add_command(new_command)

    # === END OF GROUP ===
    for section in sections:
        resource_group.add_section(section)

    return resource_group


def group_slots_by_category(slots: List[dict]):
    ctx = click.get_current_context()
    all_categories = ctx.obj.api.categories.list()

    # first find all categories that are in use in the list
    category_ids = sorted(set(s.category.id if s.category else 0 for s in slots))

    # then collect and sort all unique times
    all_times = [attr for s in slots for attr in (s.startTime, s.endTime)]
    all_times = sorted(set(all_times))

    headers = dict(time="time", relative="relative")
    for cid in category_ids:
        if cid == 0:
            headers["0"] = "no category"
        else:
            try:
                cat = next(c for c in all_categories if c.id == cid)
                headers[str(cid)] = cat.name + " " + CL.attr(cid)
            except StopIteration:
                pass

    rows = []
    for i, t in enumerate(all_times):
        row = dict()
        # pre-populate the columns - to force column order
        for cc in category_ids:
            rel_t = to_relative_time(t)
            row["time"] = CL.past(t) if t < datetime.now(timezone.utc) else CL.future(t)
            row["relative"] = (
                CL.past(rel_t) if t < datetime.now(timezone.utc) else CL.future(rel_t)
            )
            row[str(cc)] = ""

        spanning_slots = [s for s in slots if s.startTime <= t and s.endTime >= t]

        # if all slots are starting, add an empty row for readability
        if i > 0 and all(s.startTime == t for s in spanning_slots):
            r2 = copy.copy(row)
            time_diff = t - all_times[i - 1]
            r2["time"] = click.style(
                f"... {time_diff.total_seconds()} sec w/o slot ...",
                italic=True,
                fg="white",
                dim=True,
            )
            r2["relative"] = ""
            rows.append(r2)

        # are there any starting at that time?
        has_starting_slots = any(s for s in spanning_slots if s.startTime == t)

        # group by category
        for cc in category_ids:
            if cc == 0:
                related_slots_for_category = [
                    s for s in spanning_slots if s.category is None
                ]
            else:
                related_slots_for_category = [
                    s for s in spanning_slots if s.category and s.category.id == cc
                ]

            if not related_slots_for_category:
                if has_starting_slots:
                    row[str(cc)] = click.style("───" * 10, fg="white", dim="true")
                else:
                    row[str(cc)] = ""
                continue
            # if more than 1 slot related to that time for that category, one is ending, the other is starting
            if len(related_slots_for_category) > 1:
                rs = next(s for s in related_slots_for_category if s.startTime == t)
            else:
                rs = related_slots_for_category[0]

            row[str(cc)] = slot_info_for_time(rs, t, has_starting_slots)

        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))


def slot_info_for_time(slot, t, with_start_slots):
    width = 30

    if slot.endTime < datetime.now(timezone.utc):  # past slots
        if slot.type.value == "ad-break":
            color_line = functools.partial(click.style, fg="magenta")
            color_title = functools.partial(click.style, bg="white", fg="magenta")
        else:
            color_line = functools.partial(click.style, fg="blue")
            color_title = functools.partial(click.style, bg="white", fg="blue")
    else:  # future slots
        if slot.type.value == "ad-break":
            color_line = functools.partial(click.style, fg="magenta", bold=True)
            color_title = functools.partial(click.style, bg="magenta", fg="white")
        else:
            color_line = functools.partial(click.style, fg="blue", bold=True)
            color_title = functools.partial(click.style, bg="blue", fg="white")

    desc = (
        click.style(
            (
                color_title(
                    trim_or_pad(
                        " " + slot.replacement.name + " ", size=width + 3, pad=True
                    )
                )
                if slot.replacement
                else color_title(trim_or_pad(" Ad Break ", size=width + 3, pad=True))
            ),
        )
        + "\n"
        + color_line("│")
        + trim_or_pad(
            " "
            + CL.attr(slot.id)
            + "  "
            + CL.high1(seconds_to_timecode(slot.duration)),
            size=width + 1,
            pad=True,
        )
        + color_line("│")
    )

    mid_line = "│" + " " * width + "│"
    end_line = "└" + "─" * width + "╯"

    if t == slot.startTime:
        return desc
    elif t == slot.endTime:
        return color_line(end_line)
    else:
        if with_start_slots:
            return color_line(mid_line) + "\n" + color_line(mid_line)
        else:
            return color_line(mid_line)
