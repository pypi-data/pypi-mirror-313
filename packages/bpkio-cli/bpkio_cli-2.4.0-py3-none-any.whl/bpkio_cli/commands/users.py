from bpkio_api.models import User

from bpkio_cli.commands.template_crud import create_resource_group


def get_users_commands():
    return [
        create_resource_group(
            "user",
            resource_type=User,
            endpoint_path=["users"],
            aliases=["usr", "users"],
            default_fields=["id", "firstName", "lastName", "email", "creationDate"],
        )
    ]
