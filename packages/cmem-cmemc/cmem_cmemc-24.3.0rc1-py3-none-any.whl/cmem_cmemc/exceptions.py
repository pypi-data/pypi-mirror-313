"""Declares all cli exceptions."""


class InvalidConfigurationError(ValueError):
    """The configuration given was not found or is broken."""


class ServerError(ValueError):
    """The server reported an error with a process."""
