from abc import ABC, abstractmethod

from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
from mortgage_sim.utils.asserts import assert_type


class RecordTemplate(ABC):
    @classmethod
    @abstractmethod
    def get_schema(cls) -> type[SchemaTemplate]:
        raise NotImplementedError

    def __post_init__(self):
        for expected_attrs, expected_py_type in (
            self.get_schema().get_python_schema().items()
        ):
            assert_type(expected_attrs, expected_py_type)
