from typing import List

from pydantic import BaseModel

from src.schemas.event import EventSchema


class BaseWrapper(BaseModel):
    status: int = 200
    error: bool = False


class EventWrapper(BaseWrapper):
    payload: EventSchema


class EventListWrapper(BaseWrapper):
    payload: List[EventSchema]
