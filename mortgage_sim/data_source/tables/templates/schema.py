from abc import ABC, abstractmethod


class SchemaTemplate(ABC):
    @abstractmethod
    def get_polars_schema(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_python_schema(self) -> dict:
        raise NotImplementedError
