from core import logger
from core.db import filler


def prerun():
    logger.init()
    filler.fill()
