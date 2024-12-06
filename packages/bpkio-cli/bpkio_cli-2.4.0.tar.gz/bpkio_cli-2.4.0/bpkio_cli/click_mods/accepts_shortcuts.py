import cloup


class AcceptsShortcutsGroup(cloup.Group):
    def parse_args(self, ctx, args):
        # Allow a MediaMuncher only mode
        if hasattr(self, "shortcut"):
            # find the position of the first argument that isn't an option
            pos = 0
            found = False
            if len(args) > 0:
                while found is False:
                    arg = args[pos]
                    if arg.startswith("-") and arg not in ["-h", "--help"]:
                        # find corresponding option
                        option = next(
                            (
                                p
                                for p in self.get_params(ctx)
                                if (
                                    arg in p.opts
                                    or (p.count is True and arg[:2] in p.opts)
                                )
                            ),
                            None,
                        )
                        if option:
                            if option.is_flag or option.count is True:
                                pos += 1
                            else:
                                pos += 2
                    else:
                        found = True

            # insert "url" at the found position
            args.insert(pos, self.shortcut)

        return super().parse_args(ctx, args)
