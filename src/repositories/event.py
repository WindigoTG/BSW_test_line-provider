from typing import Sequence

from sqlalchemy import select, Result

from src.models import Event
from src.utils.repository import SqlAlchemyRepository


class EventRepository(SqlAlchemyRepository):
    model = Event

    async def get_all_events_before_timestamp(
        self,
        timestamp: int,
    ) -> Sequence[type(model)]:
        query = select(self.model).filter(self.model.deadline > timestamp)
        res: Result = await self.session.execute(query)
        return res.scalars().all()
