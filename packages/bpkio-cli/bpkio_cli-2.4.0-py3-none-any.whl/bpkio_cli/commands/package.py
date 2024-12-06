import json
import random
import string

import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.models.common import summary
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.logging import logger
from bpkio_cli.core.packager import PackageInstaller, ResourcePackager
from bpkio_cli.writers.colorizer import Colorizer as CL
from InquirerPy.base.control import Choice


@cloup.group(aliases=["pkg"], help="Work with reusable packages of resources")
def package():
    pass


@package.command(help="Make a package of resources")
@cloup.argument(
    "ref",
    help="A reference to a resource. Use '$' for the last resource used, or '@' for the last list or resources used",
    # default="$",
    required=False,
)
@cloup.option(
    "--save", "output_file", type=click.File("w"), required=False, default=None
)
@click.pass_obj
def make(obj: AppContext, ref: str, output_file):
    resources = []

    if ref is None:
        ref = "@"

    # if the string is an integer, retrieve the corresponding service
    if ref.isdigit():
        resources = [obj.api.services.retrieve(int(ref))]

    if ref == "$":
        resources = prompt.fuzzy(
            message="What (top-level) resources do you want to include in the package?",
            choices=[
                Choice(s, name=summary(s, with_class=True), enabled=(i == 0))
                for i, s in enumerate(obj.cache.list_resources(models_only=True))
            ],
            multiselect=True,
            keybindings={"toggle": [{"key": "right"}]},
            long_instruction="Keyboard: right arrow = toggle select/unselect; ctrl+r = toggle all",
        )

    if ref == "@":
        list = prompt.select(
            message="What list of resources to use?",
            multiselect=False,
            choices=[
                Choice(lst, name=k, enabled=(i == 0))
                for i, (k, lst) in enumerate(obj.cache.list_lists().items())
            ],
        )

        resources = prompt.fuzzy(
            message="What (top-level) resources do you want to include in the package?  ",
            choices=[Choice(s, name=summary(s, with_class=True)) for s in list],
            multiselect=True,
            keybindings={"toggle": [{"key": "right"}]},
            long_instruction="Keyboard: right arrow = toggle select/unselect; ctrl+r = toggle all",
        )

    if resources:
        package_resources(resources, obj.api, output_file)
    else:
        print(
            CL.error(
                "No corresponding resources found in the tool's history for this tenant"
            )
        )
        print(
            CL.info(
                "Use a 'get' or 'list' command to put some resources into the history first"
            )
        )


def package_resources(resources, api, output: click.File):
    packager = ResourcePackager(api)
    pkg = packager.package(root_resources=resources)

    if output:
        output.write(json.dumps(pkg, indent=2))
        logger.info(f"Package stored into {output.name}")
    else:
        print(json.dumps(pkg, indent=2))


@package.command(help="Deploy a package")
@cloup.argument(
    "file",
    type=click.File("r"),
    help="JSON File containing the package",
    required=True,
)
@cloup.option(
    "--prefix",
    type=str,
    help="Adds a prefix to the resource names. This can be used to create a duplicate of already exists (for resources that support it)",
    is_flag=False,
    flag_value="random",
    default=None,
)
@click.pass_obj
def deploy(obj: AppContext, file, prefix):
    if prefix == "random":
        prefix = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    if prefix:
        prefix = f"({prefix})"

    installer = PackageInstaller(obj.api, name_prefix=prefix)

    package = json.load(file)

    output = installer.deploy(package)

    table = [
        dict(
            status=st.name,
            resource=summary(res, with_class=True),
            message=msg,
        )
        for (res, st, msg) in output.values()
    ]

    obj.response_handler.treat_simple_list(table)
