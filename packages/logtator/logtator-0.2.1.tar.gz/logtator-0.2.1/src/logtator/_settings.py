import dataclasses
import logging

from . import formatters


@dataclasses.dataclass
class Base:
    default_level: int | str = logging.INFO
    force_default_level: bool = False
    logs_formatter: logging.Formatter = formatters.Json()
    reset_warning_filters: bool = True
