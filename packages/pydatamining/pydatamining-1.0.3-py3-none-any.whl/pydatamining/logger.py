from loguru import logger # type: ignore
import sys

def configure_logger() -> None:
    logger.remove()
    
    logger.add(sys.stdout, format="{time} - {level}: {message}", level="DEBUG")

    logger.info("Logger configured")