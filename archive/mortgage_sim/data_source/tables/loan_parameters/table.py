from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from mortgage_sim.data_source.signatures import LoanParametersTableSignature
from mortgage_sim.data_source.tables.loan_parameters.schema import (
    LoanParametersTableSchema,
)
from mortgage_sim.data_source.tables.templates.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class LoanParametersTable(TableTemplate):
    """Main LoanParameters fact table."""

    path: Path
    signature: ClassVar[type[LoanParametersTableSignature]] = (
        LoanParametersTableSignature
    )
    schema: ClassVar[type[LoanParametersTableSchema]] = LoanParametersTableSchema

    def __post_init__(self):
        assert_type(self.path, Path)
        self.signature.assert_path_endswith_signature(self.path)

    def get_path(self) -> Path:
        return self.path

    @classmethod
    def get_schema(cls) -> type[LoanParametersTableSchema]:
        return LoanParametersTableSchema

    @classmethod
    def get_signature(cls) -> type[LoanParametersTableSignature]:
        return LoanParametersTableSignature

    @classmethod
    def get_joins(cls) -> dict[str, str]:
        return {}
