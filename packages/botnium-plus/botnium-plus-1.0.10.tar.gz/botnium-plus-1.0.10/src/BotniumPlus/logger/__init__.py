import logging
from logging import handlers
import os

logger = logging.getLogger('robot')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

logFolder = os.path.join(os.getenv("LOCALAPPDATA"), 'Clicknium', 'Log')
if not os.path.exists(logFolder):
    os.makedirs(logFolder, exist_ok=True)
rotating_file_handler = handlers.TimedRotatingFileHandler(os.path.join(logFolder, 'robot.log'), when='midnight', backupCount=15, encoding='utf-8')
rotating_file_handler.setLevel(logging.DEBUG)
rotating_file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_file_handler)
logger.addHandler(stream_handler)