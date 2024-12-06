from bpkio_api.models import Category

from bpkio_cli.commands.creators.categories import create_category_command
from bpkio_cli.commands.template_crud import create_resource_group


def get_categories_command():
    return create_resource_group(
        "category",
        resource_type=Category,
        endpoint_path=["categories"],
        aliases=["cat", "categories"],
        default_fields=["id", "name", "subcategories_list"],
        extra_commands=[create_category_command()],
    )
