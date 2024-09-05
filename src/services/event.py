from typing import Any, Union
from uuid import uuid4

from sqlalchemy import Sequence

from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork


class EventService(BaseService):
    base_repository: str = 'event'

    @classmethod
    async def get_active_events(
            cls,
            uow: UnitOfWork,
            timestamp: int,
    ) -> Sequence[Any]:
        async with uow:
            _result = await uow.__dict__[
                cls.base_repository
            ].get_all_events_before_timestamp(
                timestamp,
            )
            return _result

    @classmethod
    async def update_one_by_id(
            cls,
            uow: UnitOfWork,
            _id: Union[int, str, uuid4],
            values: dict
    ) -> Any:
        for key, value in values.items():
            if value is None:
                del value[key]
        return await super().update_one_by_id(uow, _id, values)
