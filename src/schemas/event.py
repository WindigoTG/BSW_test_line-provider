import decimal
from typing import Optional

from pydantic import BaseModel, Field

from src.utils.enums import EventState


class IDEventSchema(BaseModel):
    id: int


class CreateEventSchema(BaseModel):
    coefficient: decimal.Decimal
    deadline: int
    state: EventState


class EventSchema(IDEventSchema, CreateEventSchema):
    ...


class UpdateEventSchema(IDEventSchema):
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None
