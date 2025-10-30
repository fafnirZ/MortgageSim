from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from mortgage_sim.data_source.signatures import EventsTableSignature
from mortgage_sim.data_source.tables.events.schema import EventsTableSchema
from mortgage_sim.data_source.tables.templates.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class EventsTable(TableTemplate):
    """Main events fact table."""

    path: Path
    signature: ClassVar[type[EventsTableSignature]] = EventsTableSignature
    schema: ClassVar[type[EventsTableSchema]] = EventsTableSchema

    def __post_init__(self):
        assert_type(self.path, Path)
        self.signature.assert_path_endswith_signature(self.path)

    def get_path(self) -> Path:
        return self.path

    @classmethod
    def get_schema(cls) -> type[EventsTableSchema]:
        return EventsTableSchema

    @classmethod
    def get_signature(cls) -> type[EventsTableSignature]:
        return EventsTableSignature

    @classmethod
    def get_joins(cls) -> dict[str, str]:
        return {
            "self.fk__recurring_payments": "RecurringPaymentsTable.uuid",
            "self.fk__single_payments": "SinglePaymentsTable.uuid",
            "self.fk__loan_parameters": "LoanParamatersTable.uuid",
        }
