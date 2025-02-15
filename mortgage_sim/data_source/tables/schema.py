from abc import ABC, abstractmethod


class SchemaTemplate(ABC):
    @property
    @abstractmethod
    def polars_schema(self) -> dict:
        raise NotImplementedError
