import os

import cloup
from bpkio_cli.writers.breadcrumbs import display_tip


class DefaultLastSubcommandGroup(cloup.Group):
    """allow a default command for a group"""

    def resolve_command(self, ctx, args):

        self.discover_plugins(ctx)        
            
        if args[0] not in self.list_commands(ctx) and args[0] not in self.alias2name:
            last_command = self._get_last_command()
            if last_command:
                display_tip(
                    f"No sub-command provided. Re-using last command: '{last_command}'"
                )
                args.insert(0, last_command)

        return super(DefaultLastSubcommandGroup, self).resolve_command(ctx, args)

    def _get_last_command(self):
        if os.path.exists(".last_command"):
            with open(".last_command") as f:
                return f.read()
        return None
