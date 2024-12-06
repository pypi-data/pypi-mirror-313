from abc import ABC
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class ValueObject(BaseModel, ABC):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
