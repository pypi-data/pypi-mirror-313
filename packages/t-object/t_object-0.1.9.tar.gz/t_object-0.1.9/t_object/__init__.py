"""Top-level package for t_object."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "0.1.9"

from .config_enums import Extra, RevalidateInstances, SerJsonTimedelta, SerJsonInfNan
from .t_object import ThoughtfulObject
from .builder import build_custom_t_object

__all__ = [
    "ThoughtfulObject",
    "build_custom_t_object",
    "Extra",
    "RevalidateInstances",
    "SerJsonTimedelta",
    "SerJsonInfNan",
]
