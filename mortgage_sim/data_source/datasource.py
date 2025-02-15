from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from mortgage_sim.data_source.signatures import DataSourceSignature
from mortgage_sim.data_source.tables.events.table import EventsTable
from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class DataSource:
    path: Path
    signature: ClassVar[type[DataSourceSignature]] = DataSourceSignature

    @classmethod
    def init(cls, *, path: Path):
        assert_type(path, Path)
        if path.exists():
            raise FileExistsError(
                f"Datasource cannot be created at path: {path}"
                "since something already exists there"
            )

        # init data_source
        cls.__init_datasource(path=path)

        return cls(path=path)

    @classmethod
    def __init_datasource(cls, *, path: Path):
        # assert ends with datasource signature
        cls.signature.assert_path_endswith_signature(path)

        # create datasource
        path.mkdir()

        # create events table
        EventsTable.create(path=path / EventsTable.signature.get_signature())

    @classmethod
    def from_path(cls, *, path: Path):
        assert_type(path, Path)

        cls.signature.assert_path_endswith_signature(path)

        if not path.is_dir():
            raise FileNotFoundError(
                f"Datasource cannot be instantiated at path: {path}"
                "It either does not exist or is not a directory"
            )
        return cls(path=path)

    #
    # instance methods
    #

    @property
    def events_table(self):
        return EventsTable(path=self.path / EventsTable.signature.get_signature())
