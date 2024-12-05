"""cmemc Click Command"""

from click_help_colors import HelpColorsCommand


class CmemcCommand(HelpColorsCommand):
    """Wrapper click.Command class to have a single extension point.

    Currently, wrapped click extensions and additional group features:#
    - click-help-colors: https://github.com/click-contrib/click-help-colors
    """

    color_for_headers = "yellow"
    color_for_options = "green"

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        """Init a cmemc group command."""
        kwargs.setdefault("help_headers_color", self.color_for_headers)
        kwargs.setdefault("help_options_color", self.color_for_options)
        super().__init__(*args, **kwargs)
