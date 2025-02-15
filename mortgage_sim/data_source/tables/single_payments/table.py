from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from mortgage_sim.data_source.signatures import SinglePaymentsTableSignature
from mortgage_sim.data_source.tables.single_payments.schema import (
    SinglePaymentsTableSchema,
)
from mortgage_sim.data_source.tables.templates.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class SinglePaymentsTable(TableTemplate):
    """Main events fact table."""

    path: Path

    def __post_init__(self):
        assert_type(self.path, Path)
        self.get_signature().assert_path_endswith_signature(self.path)

    def get_path(self) -> Path:
        return self.path

    @classmethod
    def get_signature(cls) -> type[SinglePaymentsTableSignature]:
        return SinglePaymentsTableSignature

    @classmethod
    def get_schema(cls) -> type[SinglePaymentsTableSchema]:
        return SinglePaymentsTableSchema

    @classmethod
    def get_joins(cls) -> dict[str, str]:
        return {}
