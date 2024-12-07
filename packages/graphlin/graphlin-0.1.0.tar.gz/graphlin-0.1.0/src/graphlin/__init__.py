__version__ = "0.1.0"


from graphlin.configuration import settings
from graphlin.logging import setup_logging

logger = setup_logging(log_level=settings.LOG_LEVEL)
