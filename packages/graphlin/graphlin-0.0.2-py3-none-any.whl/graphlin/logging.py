import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logging(log_level: str = "INFO"):
    log_int = getattr(logging, log_level)
    root_logger = logging.getLogger("graphlin")
    root_logger.setLevel(log_int)
    handler = RichHandler(console=console)
    handler.setLevel(log_int)
    root_logger.addHandler(handler)
    return root_logger
