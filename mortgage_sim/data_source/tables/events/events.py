from __future__ import annotations
from pathlib import Path
from typing import ClassVar
from mortgage_sim.data_source.signatures import EventsTableSignature
from mortgage_sim.data_source.tables.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type


class EventsTable(TableTemplate):
    """Main events fact table."""

    path: Path
    signature: ClassVar[type[EventsTableSignature]] = EventsTableSignature

    @classmethod
    def create(cls, *, path: Path) -> EventsTable:
        assert_type(path, Path)
        cls.signature.assert_path_endswith_signature(path)
        if path.is_file():
            raise FileExistsError(
                f"Cannot Create EventsTable, file already exists at {path}"
            )

        # create empty table
        return cls(path=path)

    def __create_empty_table(cls):
        # TODO
        pass
