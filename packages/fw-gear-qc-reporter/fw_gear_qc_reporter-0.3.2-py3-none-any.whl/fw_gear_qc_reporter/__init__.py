"""The fw_gear_qc_reporter package."""

from importlib.metadata import version

NAME = __name__

try:
    __version__ = version(__package__)
except:  # noqa: E722
    __version__ = "0.1.0"
