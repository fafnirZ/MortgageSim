from abc import ABC, abstractmethod
from pathlib import Path
import polars as pl

from mortgage_sim.data_source.tables.schema import SchemaTemplate


class TableTemplate(ABC):
    @property
    @abstractmethod
    def path(self) -> Path:
        raise NotImplementedError

    @property
    @abstractmethod
    def schema(self) -> SchemaTemplate:
        raise NotImplementedError

    def scan_parquet(self) -> pl.LazyFrame:
        return pl.scan_parquet(str(self.path))
