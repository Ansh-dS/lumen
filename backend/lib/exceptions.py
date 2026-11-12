class LumenError(Exception):
    """Contains all errors contianed by this application."""


class ConfigError(LumenError):
    """Raised when configuration is missing or invalid."""
