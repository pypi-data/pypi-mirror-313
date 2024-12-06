from typing import Tuple

import bpkio_cli.click_mods.resource_commands as bic_res_cmd
import click
import cloup
from bpkio_api.models.Categories import CategoryIn, SubCategory
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.utils import prompt


def create_category_command():
    # COMMAND: CREATE
    @bic_res_cmd.command(help="Create a Category", takes_id_arg=False)
    @cloup.argument("name", required=True)
    @cloup.option(
        "--sub",
        help="Optional list of subcategories. You can either add comma-separated values or blank-separated values, or leave blank to get a prompt",
        required=False,
        cls=OptionEatAll,
        type=tuple,
        is_flag=False,
        flag_value=tuple(),
    )
    @click.pass_obj
    def create(obj: AppContext, name, sub):
        create_category_with_prompts(obj, name, sub)

    return create


def create_category_with_prompts(
    app_context: AppContext, name: str, subcategories: Tuple[str]
):
    category_in = CategoryIn(name=name)

    if subcategories:
        # Trick to allow --sub to be used as a flag without value
        subcategories = [sub for sub in subcategories if isinstance(sub, str)]

        subcat_all = " ".join(subcategories)
        # then we split again
        for char in [",", ";", " "]:
            if char in subcat_all:
                subcategories = [subcat.strip() for subcat in subcat_all.split(char)]
                break

        if len(subcategories):
            category_in.subcategories = [
                SubCategory(key="zip", value=subcat) for subcat in subcategories
            ]

        else:
            subcats = []

            subcategory_key = prompt.text(
                message="Key",
                default="zip",
                long_instruction="There is currently no use case for subcategories with a different key than 'zip'",
            )

            while True:
                subcategory_name = prompt.text(
                    message="Subcategory name",
                    default="",
                    long_instruction="To finish adding subcategories, just hit enter on a blank line",
                )
                if not subcategory_name:
                    break

                subcats.append(SubCategory(key=subcategory_key, value=subcategory_name))

            category_in.subcategories = subcats

    category_out = app_context.api.categories.create(category_in)

    app_context.response_handler.treat_single_resource(category_out)
