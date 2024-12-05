from importlib.metadata import PackageNotFoundError, version

from .serp import GoogleSearchAPI

try:
    __version__ = version("brd_client")
except PackageNotFoundError:
    # package is not installed
    pass
