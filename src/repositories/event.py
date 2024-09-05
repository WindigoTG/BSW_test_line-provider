from src.models import Event
from src.utils.repository import SqlAlchemyRepository


class EventRepository(SqlAlchemyRepository):
    model = Event
