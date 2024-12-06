from pathlib import Path
from typing import Final

from .domain.entity import Aggregate, Entity
from .domain.vo import ValueObject

__all__ = (
    "DIRECTORY",
    "Aggregate",
    "Entity",
    "ValueObject",
)

DIRECTORY: Final[Path] = Path(__file__).resolve().parent
