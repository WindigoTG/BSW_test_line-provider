from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.utils.enums import EventState


class IDEventSchema(BaseModel):
    id: int


class CreateEventSchema(BaseModel):
    coefficient: Decimal = Field(decimal_places=2, gt=0)
    deadline: int
    state: EventState


class EventSchema(IDEventSchema, CreateEventSchema):
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('coefficient')
    def serialize_coefficient(self, coefficient: Decimal, _info):
        return str(coefficient)

    @field_serializer('state')
    def serialize_state(self, state: EventState, _info):
        return state.value


class UpdateEventSchema(IDEventSchema):
    coefficient: Optional[Decimal] = Field(
        default=None,
        decimal_places=2,
        gt=0,
    )
    deadline: Optional[int] = None
    state: Optional[EventState] = None
