from dataclasses import dataclass
from mortgage_sim.data_source.tables.events.schema import EventsTableSchema
from mortgage_sim.data_source.tables.templates.record import RecordTemplate


@dataclass
class EventsTableRecord(RecordTemplate):
    @classmethod
    def get_schema(cls) -> type[EventsTableSchema]:
        return EventsTableSchema
