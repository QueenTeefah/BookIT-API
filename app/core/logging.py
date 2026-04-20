from loguru import logger
from .config import settings
import sys

logger.remove()
logger.add(sys.stdout, level=settings.LOG_LEVEL)
