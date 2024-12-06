# read version from installed package if possible
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("energy_manager")
except PackageNotFoundError:
    __version__ = "0.1.0"
