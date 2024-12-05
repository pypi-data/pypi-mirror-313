"""cmemc Click Command Group"""

from click_didyoumean import DYMGroup
from click_help_colors import HelpColorsGroup


class CmemcGroup(HelpColorsGroup, DYMGroup):
    """Wrapper click.Group class to have a single extension point.

    Currently, wrapped click extensions and additional group features:#
    - click-help-colors: https://github.com/click-contrib/click-help-colors
    """

    color_for_command_groups = "white"
    color_for_writing_commands = "red"
    color_for_headers = "yellow"
    color_for_options = "green"

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        """Init a cmemc group command group."""
        # set default colors
        kwargs.setdefault("help_headers_color", self.color_for_headers)
        kwargs.setdefault("help_options_color", self.color_for_options)
        kwargs.setdefault(
            "help_options_custom_colors",
            {
                "bootstrap": self.color_for_writing_commands,
                "showcase": self.color_for_writing_commands,
                "delete": self.color_for_writing_commands,
                "password": self.color_for_writing_commands,
                "secret": self.color_for_writing_commands,
                "upload": self.color_for_writing_commands,
                "import": self.color_for_writing_commands,
                "create": self.color_for_writing_commands,
                "enable": self.color_for_writing_commands,
                "disable": self.color_for_writing_commands,
                "execute": self.color_for_writing_commands,
                "replay": self.color_for_writing_commands,
                "io": self.color_for_writing_commands,
                "install": self.color_for_writing_commands,
                "uninstall": self.color_for_writing_commands,
                "reload": self.color_for_writing_commands,
                "update": self.color_for_writing_commands,
                "eval": self.color_for_writing_commands,
                "cancel": self.color_for_writing_commands,
                "admin": self.color_for_command_groups,
                "user": self.color_for_command_groups,
                "store": self.color_for_command_groups,
                "metrics": self.color_for_command_groups,
                "config": self.color_for_command_groups,
                "dataset": self.color_for_command_groups,
                "graph": self.color_for_command_groups,
                "project": self.color_for_command_groups,
                "query": self.color_for_command_groups,
                "scheduler": self.color_for_command_groups,
                "vocabulary": self.color_for_command_groups,
                "workflow": self.color_for_command_groups,
                "workspace": self.color_for_command_groups,
                "python": self.color_for_command_groups,
                "cache": self.color_for_command_groups,
                "resource": self.color_for_command_groups,
                "acl": self.color_for_command_groups,
                "client": self.color_for_command_groups,
                "variable": self.color_for_command_groups,
                "validation": self.color_for_command_groups,
                "migrate": self.color_for_writing_commands,
                "migrations": self.color_for_command_groups,
            },
        )
        super().__init__(*args, **kwargs)
