from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from mortgage_sim.data_source.signatures import EventsTableSignature
from mortgage_sim.data_source.tables.events.schema import EventsTableSchema
from mortgage_sim.data_source.tables.templates.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type
import polars as pl


@dataclass(frozen=True)
class EventsTable(TableTemplate):
    """Main events fact table."""

    path: Path
    signature: ClassVar[type[EventsTableSignature]] = EventsTableSignature
    schema: ClassVar[type[EventsTableSchema]] = EventsTableSchema

    def __post_init__(self):
        assert_type(self.path, Path)
        self.signature.assert_path_endswith_signature(self.path)

    @classmethod
    def create(cls, *, path: Path) -> EventsTable:
        assert_type(path, Path)
        cls.signature.assert_path_endswith_signature(path)
        if path.is_file():
            raise FileExistsError(
                f"Cannot Create EventsTable, file already exists at {path}"
            )

        # create empty table
        cls.__create_empty_table(path=path)

        return cls(path=path)

    @classmethod
    def __create_empty_table(cls, *, path: Path):
        assert_type(path, Path)
        df = pl.DataFrame(
            {},
            schema=cls.schema.get_polars_schema(),
        )
        df.write_parquet(path)

    def get_path(self) -> Path:
        return self.path
