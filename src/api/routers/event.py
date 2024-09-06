import time

from fastapi import APIRouter, Depends

from src.schemas.event import CreateEventSchema, EventSchema, UpdateEventSchema
from src.schemas.wrapper import BaseWrapper, EventListWrapper, EventWrapper
from src.services.event import EventService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter()


@router.get(
    '/events',
    response_model=EventListWrapper,
    summary="Get list of active events."
)
async def get_events(uow: UnitOfWork = Depends(UnitOfWork)):
    """Get list of active events."""
    events = await EventService.get_active_events(uow, int(time.time()))
    return EventListWrapper(
        payload=[
            EventSchema.model_validate(event)
            for event in events
        ]
    )


@router.post(
    '/event',
    response_model=EventWrapper,
    summary="Create new event.",
)
async def create_event(
    event: CreateEventSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """
    Create new event.

    Body params:
    - **coefficient**: Bet coefficient for the event.
    - **deadline**: Timestamp of betting dedline.
    - **state**: State of the event.
    """
    event = await EventService.add_one_and_get_obj(
        uow,
        coefficient=event.coefficient,
        deadline=event.deadline,
        state=event.state,
    )
    return EventWrapper(status=201, payload=EventSchema.model_validate(event))


@router.put(
    '/event',
    response_model=EventWrapper,
    summary="Update event data.",
)
async def update_event(
    event: UpdateEventSchema,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    """
    Update event data

    Body params:
    - **id**: Id of the event.
    - **coefficient**: Bet coefficient for the event.
    - **deadline**: Timestamp of betting dedline.
    - **state**: State of the event.
    """
    event = await EventService.update_one_by_id(
        uow,
        event.id,
        {
            "coefficient": event.coefficient,
            "deadline": event.deadline,
            "state": event.state,
        }
    )
    if not event:
        return BaseWrapper(error=True, status=404)
    return EventWrapper(status=200, payload=EventSchema.model_validate(event))


@router.get(
    '/event/{event_id}',
    summary="Get a single event by id."
)
async def get_event(event_id: int, uow: UnitOfWork = Depends(UnitOfWork)):
    """
    Get a single event by id.

    Path params:
    - **event_id**: Id of the event.
    """
    event = await EventService.get_by_query_one_or_none(uow, id=event_id)
    if not event:
        return BaseWrapper(error=True, status=404)
    return EventWrapper(payload=EventSchema.model_validate(event))
