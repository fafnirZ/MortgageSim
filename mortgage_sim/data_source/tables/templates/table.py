from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import polars as pl

from mortgage_sim.data_source.signatures import SignatureTemplate
from mortgage_sim.data_source.tables.templates.record import RecordTemplate
from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
from mortgage_sim.utils.asserts import assert_type


# stubs for enabling LSP
class TableProtocol:
    def get_path(self) -> Path: ...

    @classmethod
    def get_schema(self) -> SchemaTemplate: ...

    @classmethod
    def get_signature(cls) -> type[SignatureTemplate]: ...

    def scan_csv(self) -> pl.LazyFrame: ...

    @classmethod
    def create(cls, *, path: Path) -> TableTemplate: ...

    @classmethod
    def __create_empty_table(cls, *, path: Path): ...


class TableTemplate(ABC):
    #
    # abstract
    #
    @abstractmethod
    def get_path(self) -> Path:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_schema(cls) -> SchemaTemplate:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_signature(cls) -> type[SignatureTemplate]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_joins(cls) -> dict[str, str]:
        raise NotImplementedError

    #
    # concrete methods
    #

    def scan_csv(self) -> pl.LazyFrame:
        return pl.scan_csv(str(self.get_path()))

    @classmethod
    def create(cls: TableProtocol, *, path: Path) -> TableTemplate:
        assert_type(path, Path)

        print()
        cls.get_signature().assert_path_endswith_signature(path)
        if path.is_file():
            raise FileExistsError(
                f"Cannot Create EventsTable, file already exists at {path}"
            )

        # create empty table
        cls.__create_empty_table(path=path)

        return cls(path=path)

    @classmethod
    def __create_empty_table(cls: TableProtocol, *, path: Path):
        assert_type(path, Path)
        df = pl.DataFrame(
            {},
            schema=cls.get_schema().get_polars_schema(),
        )
        df.write_parquet(path)

    def append_record(self, *, record: RecordTemplate):
        if record.get_schema() != self.get_schema():
            raise AssertionError(
                "Cannot append a record if schema does not match table\n"
                f"Table: {self.get_schema()}\n"
                f"Record: {record.get_schema()}\n"
            )

        # NOTE this only works for CSV datafiles
        with self.get_path().open("a") as f:
            f.append(record.to_csv())
