from loguru import logger
import sys


def config() -> None:
    logger.remove()
    logger.add(sink=sys.stderr, level='TRACE',
               format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level></w>')
