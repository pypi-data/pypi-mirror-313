from __future__ import annotations

import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

from module_qc_database_tools._version import __version__

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources
data = resources.files("module_qc_database_tools") / "data"

handler = RichHandler(markup=True, rich_tracebacks=True, console=Console(stderr=True))
formatter = logging.Formatter(fmt="%(message)s", datefmt="[%X]")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

__all__ = ("__version__", "data")
