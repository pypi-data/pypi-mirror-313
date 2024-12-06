import logging
from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if the project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .core import WeightedSampleStatistics as WeightedSampleStatistics

# Create a logger for the package
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Set the logging level

# Create a console handler and set the level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)