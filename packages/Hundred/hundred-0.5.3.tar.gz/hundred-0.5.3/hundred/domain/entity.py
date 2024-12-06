from abc import ABC
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel, ABC):
    id: UUID = Field(frozen=True)

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)


class Aggregate(Entity, ABC): ...
