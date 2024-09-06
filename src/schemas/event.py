from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.utils.enums import EventState


class IDEventSchema(BaseModel):
    id: int


class CreateEventSchema(BaseModel):
    coefficient: Decimal = Field(decimal_places=2, gt=0)
    deadline: int
    state: EventState


class EventSchema(IDEventSchema, CreateEventSchema):
    model_config = ConfigDict(from_attributes=True)


class UpdateEventSchema(IDEventSchema):
    coefficient: Optional[Decimal] = Field(
        default=None,
        decimal_places=2,
        gt=0,
    )
    deadline: Optional[int] = None
    state: Optional[EventState] = None
