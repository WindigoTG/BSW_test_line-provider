import decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.utils.enums import EventState


class IDEventSchema(BaseModel):
    id: int


class CreateEventSchema(BaseModel):
    coefficient: decimal.Decimal
    deadline: int
    state: EventState


class EventSchema(IDEventSchema, CreateEventSchema):
    model_config = ConfigDict(from_attributes=True)


class UpdateEventSchema(IDEventSchema):
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None
