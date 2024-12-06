import base64
import os

import click
from bpkio_api.models.common import BaseResource
from pydantic import HttpUrl


class OutputStore:

    @staticmethod
    def get_output_folder(*sub_folders):
        sub_folders = [s for s in sub_folders if s is not None]

        folders = [os.getcwd(), "bic-outputs"]
        ctx = click.get_current_context()
        if res := ctx.obj.current_resource:
            if isinstance(res, BaseResource):
                folders.append(f"{res.__class__.__name__}.{res.id}")
            elif isinstance(res, HttpUrl):
                path = base64.b64encode(
                    (res.path + "?" + str(res.query)).encode("ascii")
                ).decode("ascii")
                folders.append(f"{res.host}_{path}")

        folders.extend(sub_folders)

        path = os.path.join(*folders)
        os.makedirs(path, exist_ok=True)

        return path
