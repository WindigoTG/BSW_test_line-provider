import json
from typing import Any, Union
from uuid import uuid4

import aiohttp
from pydantic import ValidationError
from sqlalchemy import Sequence

from src.schemas.event import EventSchema
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork

from src.config import settings


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

        _obj = await super().update_one_by_id(uow, _id, values)

        await cls._send_event_update_notification(_obj)

        return _obj

    @classmethod
    async def _send_event_update_notification(cls, event: Any):
        try:
            event = EventSchema.model_validate(event)
        except ValidationError:
            return

        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.STATE_CHANGE_NOTIFY_URL,
                json=event.model_dump(),
            ) as response:
                # TODO: обработка возможных ошибок
                ...
