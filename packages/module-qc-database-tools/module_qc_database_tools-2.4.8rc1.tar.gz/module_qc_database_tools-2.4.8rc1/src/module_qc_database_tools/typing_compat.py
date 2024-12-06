"""
Typing helpers.
"""

from __future__ import annotations

import sys
from typing import Any, Literal

if sys.version_info >= (3, 9):
    from typing import Annotated

    Dict = dict
else:
    from typing import Dict

    from typing_extensions import Annotated

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

LocalDBComponent: TypeAlias = Dict[str, Any]
ProdDBComponent: TypeAlias = Dict[str, Any]
ModuleType: TypeAlias = Literal["single", "quad", "triplet"]

__all__ = ("Annotated",)
