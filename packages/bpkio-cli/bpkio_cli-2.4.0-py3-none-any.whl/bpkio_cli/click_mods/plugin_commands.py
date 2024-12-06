import cloup

import bpkio_cli.click_mods.resource_commands as bic_res_cmd


class PluginCommand(bic_res_cmd.ResourceSubCommand):
    def __init__(self, *args, admin_only: bool = False, scopes: list = [], allow_package: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.scopes = scopes or []
        self.admin_only = admin_only
        self.allow_package = allow_package


class PluginGroup(bic_res_cmd.ResourceSubCommand, cloup.Group):
    def __init__(self, *args, admin_only: bool = False, scopes: list = [], allow_package: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.scopes = scopes or []
        self.admin_only = admin_only
        self.allow_package = allow_package


def command(name=None, cls=None, scopes: list = [], admin_only: bool = False, allow_package: bool = True, **attrs):
    if cls is None:
        cls = PluginCommand

    def decorator(f):
        cmd = cloup.command(name=name, cls=cls, **attrs)(f)
        cmd.scopes = scopes
        cmd.admin_only = admin_only
        cmd.allow_package = allow_package
        return cmd

    return decorator


def group(name=None, cls=None, scopes: list = [], admin_only: bool = False, allow_package: bool = True, **attrs):
    if cls is None:
        cls = PluginGroup

    def decorator(f):
        grp = cloup.group(name=name, cls=cls, **attrs)(f)
        grp.scopes = scopes
        grp.admin_only = admin_only
        grp.allow_package = allow_package
        return grp

    return decorator
