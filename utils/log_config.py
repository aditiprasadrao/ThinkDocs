from loguru import logger
from config import LOG_FILE
import os

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logger.remove()
logger.add(LOG_FILE, level="INFO")
