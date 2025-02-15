from abc import ABC, abstractmethod
from pathlib import Path
import polars as pl

from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate


class TableTemplate(ABC):
    @abstractmethod
    def get_path(self) -> Path:
        raise NotImplementedError

    @property
    @abstractmethod
    def schema(self) -> SchemaTemplate:
        raise NotImplementedError

    def scan_parquet(self) -> pl.LazyFrame:
        return pl.scan_parquet(str(self.get_path()))
