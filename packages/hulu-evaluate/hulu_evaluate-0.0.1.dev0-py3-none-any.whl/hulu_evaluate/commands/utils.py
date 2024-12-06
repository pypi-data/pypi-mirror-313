import argparse


class _StoreAction(argparse.Action):
    """
    Custom action that allows for `-` or `_` to be passed in for an argument.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_option_strings = []
        for option_string in self.option_strings:
            new_option_strings.append(option_string)
            if "_" in option_string[2:]:
                # Add `-` version to the option string
                new_option_strings.append(option_string.replace("_", "-"))
        self.option_strings = new_option_strings

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class _StoreConstAction(_StoreAction):
    """
    Same as `argparse._StoreConstAction` but uses the custom `_StoreAction`.
    """

    def __init__(self, option_strings, dest, const, default=None, required=False, help=None):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


class _StoreTrueAction(_StoreConstAction):
    """
    Same as `argparse._StoreTrueAction` but uses the custom `_StoreConstAction`.
    """

    def __init__(
        self,
        option_strings,
        dest,
        default=None,
        required=False,
        help=None,
    ):
        super().__init__(
            option_strings=option_strings, dest=dest, const=True, default=default, required=required, help=help
        )


class CustomArgumentGroup(argparse._ArgumentGroup):
    """
    Custom argument group that allows for the use of `-` or `_` in arguments passed and overrides the help for each
    when applicable.
    """

    def _add_action(self, action):
        args = vars(action)
        if isinstance(action, argparse._StoreTrueAction):
            action = _StoreTrueAction(
                args["option_strings"], args["dest"], args["default"], args["required"], args["help"]
            )
        elif isinstance(action, argparse._StoreConstAction):
            action = _StoreConstAction(
                args["option_strings"],
                args["dest"],
                args["const"],
                args["default"],
                args["required"],
                args["help"],
            )
        elif isinstance(action, argparse._StoreAction):
            action = _StoreAction(**args)
        action = super()._add_action(action)
        return action


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Custom argument parser that allows for the use of `-` or `_` in arguments passed and overrides the help for each
    when applicable.
    """

    def add_argument(self, *args, **kwargs):
        if "action" in kwargs:
            # Translate action -> class
            if kwargs["action"] == "store_true":
                kwargs["action"] = _StoreTrueAction
        else:
            kwargs["action"] = _StoreAction
        super().add_argument(*args, **kwargs)

    def add_argument_group(self, *args, **kwargs):
        group = CustomArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        return group