import logging

from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except:
    __version__ = "#N/A"

del metadata  # optional, avoids polluting the results of dir(__package__)

logger = logging.getLogger("dbworkload")
# logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] (%(processName)s %(threadName)s) %(module)s:%(lineno)d: %(message)s"
)
sh.setFormatter(formatter)
logger.addHandler(sh)
