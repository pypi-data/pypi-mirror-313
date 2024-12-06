import json
import os
import subprocess
import tempfile

import click
from bpkio_cli.core.config_provider import CONFIG
from pydantic import BaseModel


def edit_payload(payload: object, is_json=False):
    if isinstance(payload, BaseModel):
        payload_str = json.dumps(json.loads(payload.json()), indent=2)
    else:
        if is_json:
            payload_str = json.dumps(payload, indent=2)
        else:
            payload_str = str(payload)

    editor = CONFIG.get("editor")
    if editor in ["vi", "vim", "nano", "nvim"]:
        updated_payload = click.edit(payload_str, editor=editor, require_save=False)
    else:
        updated_payload = _edit_in_external_editor(payload_str, editor=editor)

    if updated_payload is not None:
        if isinstance(payload, BaseModel):
            # reload as JSON
            updated_payload = payload.parse_raw(updated_payload)

        return updated_payload


def _edit_in_external_editor(initial_message, editor):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        tf.write(initial_message.encode())
        tf.close()
        # The command to open the editor
        command = [editor, tf.name]
        # Call the command
        subprocess.call(command)
        # Ask the user to confirm
        try:
            input(
                "Press hit enter when you have finished editing the file, or cmd/ctrl+c to cancel the operation.\n"
            )
            # Read the file again
            with open(tf.name, "r") as f:
                edited_message = f.read()
            return edited_message

        except KeyboardInterrupt:
            click.secho("Operation cancelled", fg="red")
            raise click.Abort()

        finally:
            # Ensure the temporary file is deleted
            os.unlink(tf.name)
