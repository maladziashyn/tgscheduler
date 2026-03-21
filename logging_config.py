import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from time import gmtime

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
formatter = logging.Formatter(
    "%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)
logging.Formatter.converter = gmtime


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    file_handler = TimedRotatingFileHandler(
        filename=BASE_DIR / "log" / (name + ".log"),
        when="W0",      # Rotate every week (W0 = Monday)
        interval=1,     # Every 1 week
        backupCount=13, # Keep last N weeks of logs
    )
    console_handler = logging.StreamHandler()
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

