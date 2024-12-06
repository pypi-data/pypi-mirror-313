import json
import subprocess
from datetime import datetime, timezone

from bpkio_api.defaults import DEFAULT_FQDN
from loguru import logger

from bpkio_cli.utils import prompt
from bpkio_cli.writers.breadcrumbs import display_error, display_ok


def is_op_secret(secret: str):
    return secret.strip().strip('"').startswith("op://")

def get_accounts():
    output = subprocess.run(
        ["op", "account", "list", "--format", "json"], capture_output=True, text=True
    )
    return json.loads(output.stdout.strip())


def get_op_vaults(account: dict):
    output = subprocess.run(
        [
            "op",
            "vault",
            "list",
            "--format",
            "json",
            "--account",
            account["account_uuid"],
        ],
        capture_output=True,
        text=True,
    )
    return json.loads(output.stdout.strip())


def get_all_op_vaults():
    accounts = get_accounts()
    all_vaults = []
    for account in accounts:
        vaults = get_op_vaults(account)
        for v in vaults:
            v["account_email"] = account["email"]
            v["account_uuid"] = account["account_uuid"]
            v["vault_label"] = v["name"]
            if len(accounts) > 1:
                v["vault_label"] = f"{v['vault_label']} ({v['account_email']})"
            all_vaults.append(v)
    return all_vaults



def list_all_candidate_items():
    all_vaults = get_all_op_vaults()
    vault = prompt.fuzzy(
        message="Select a vault",
        choices=[prompt.Choice(name=v["vault_label"], value=v) for v in all_vaults],
    )

    output = subprocess.run(
        [
            "op",
            "item",
            "list",
            "--vault",
            vault["id"],
            "--account",
            vault["account_uuid"],
            "--categories",
            "API Credential",
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    j = json.loads(output.stdout.strip())
    for i in j:
        i["vault"]['account_uuid'] = vault['account_uuid']

    return j


def get_detailed_item(item_id: str, account_uuid: str, vault_id: str):
    output = subprocess.run(
        [
            "op",
            "item",
            "get",
            item_id,
            "--account",
            account_uuid,
            "--vault",
            vault_id,
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
    )
    return json.loads(output.stdout.strip())


def store_api_key_in_op(
    api_key: str,
    tenant_label: str,
    tenant_name: str,
    tenant_id: int,
    fqdn: str,
    expiration: str = None,
    valid_from: str = None,
):
    all_vaults = get_all_op_vaults()

    # Prompt the user to select a vault
    vault = prompt.fuzzy(
        message="Select a vault",
        choices=[prompt.Choice(name=v["vault_label"], value=v) for v in all_vaults],
    )

    title = f"{tenant_label}"
    if "@" not in tenant_label:
        if fqdn == DEFAULT_FQDN:
            title += " @ prod"
        else:
            title += f" @ {fqdn.split('.')[0].replace('api','')}"

    attrs = {
        "credential": api_key,
        "type": "bearer",
        "Tenant Info.platform[text]": fqdn,
        "Tenant Info.id[text]": tenant_id,
        "Tenant Info.name[text]": tenant_name,
    }

    attrs["valid from"] = (
        datetime.fromtimestamp(valid_from, tz=timezone.utc).date().strftime("%Y-%m-%d")
    )

    if expiration:
        attrs["expires"] = (
            datetime.fromtimestamp(expiration, tz=timezone.utc)
            .date()
            .strftime("%Y-%m-%d")
        )
    else:
        attrs["expires"] = "2050-12-31"

    attribute_strings = [f"{k}={v}" for k, v in attrs.items()]

    # Store the API key in the vault
    try:
        command = [
            "op",
            "item",
            "create",
            "--account",
            vault["account_uuid"],
            "--category",
            "API Credential",
            "--vault",
            vault["id"],
            "--title",
            title,
            *attribute_strings,
            "--tags",
            "Added by broadpeak.io CLI",
            "--format",
            "json",
        ]
        out = subprocess.run(command, capture_output=True, text=True)
        item = json.loads(out.stdout.strip())
    except json.JSONDecodeError as e:
        display_error(f"Failed to store API key in 1Password: {e}")
        return api_key

    item_url = f"op://{vault['id']}/{item['id']}/credential"
    display_ok(
        f"Tenant info and API key stored in 1Password vault under name: {item['title']}"
    )
    return item_url


def is_op_cli_installed():
    try:
        # Try running `op --version` to check if the CLI is installed
        result = subprocess.run(
            ["op", "--version"], capture_output=True, text=True, check=True
        )
        logger.debug(f"1Password CLI is installed. Version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        # `op` command not found
        logger.debug("1Password CLI is not installed.")
        return False
    except subprocess.CalledProcessError:
        # Command found, but failed for some other reason
        logger.debug("1Password CLI is installed but returned an error.")
        return True
