from sqlalchemy import DECIMAL, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.custom_types.custom_types import int_pk_T
from src.models import BaseModel
from src.utils.enums import EventState


class Event(BaseModel):
    __tablename__ = "events"

    id: Mapped[int_pk_T]
    coefficient: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    deadline: Mapped[int]
    state: Mapped[int] = mapped_column(Enum(EventState))
