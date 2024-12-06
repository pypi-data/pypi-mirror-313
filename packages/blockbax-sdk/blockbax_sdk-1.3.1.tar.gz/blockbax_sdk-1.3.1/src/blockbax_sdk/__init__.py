"""Blockbax Python SDK"""
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__: str = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

import logging
from .client import HttpClient
from . import models
from . import errors
from .models import type_hints

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "HttpClient",
    "models",
    "errors",
    "type_hints",
]
