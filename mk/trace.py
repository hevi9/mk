from loguru import logger

def t(*args, **kwargs):
    logger.trace(f"{kwargs}", kwargs=kwargs)