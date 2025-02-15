from abc import ABC, abstractmethod

from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
from mortgage_sim.utils.asserts import assert_type

import polars as pl


class RecordTemplate(ABC):
    @classmethod
    @abstractmethod
    def get_schema(cls) -> type[SchemaTemplate]:
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        #
        # disallow args
        #
        if len(args) > 0:
            raise ValueError("No argument initialisation allowed.")

        #
        # asserts no less or more attributes declared
        #
        if kwargs.keys() - self.get_schema().get_polars_schema().keys() != set():
            raise ValueError(
                "Invalid Kwargs\n"
                f"Expected: {self.get_schema().get_polars_schema().keys()}\n"
                f"Got: {kwargs.keys()}\n"
            )

        # dynamically setting values
        # based on kwargs which has been
        # validated against schema.
        for attr, attr_val in kwargs.items():
            setattr(self, attr, attr_val)

        #
        # asserts types are according to schema
        #
        for expected_attr, expected_py_type in (
            self.get_schema().get_python_schema().items()
        ):
            attr_val = getattr(self, expected_attr)
            assert_type(attr_val, expected_py_type)

    def to_df(self) -> pl.DataFrame:
        _d = {
            col_name: getattr(self, col_name)
            for col_name in self.get_schema().get_python_schema().keys()
        }

        return pl.DataFrame(_d, schema=self.get_schema().get_polars_schema())

    # def to_csv(self, append_newline: bool = True) -> str:
    #     _str = ""
    #     for col_name in self.get_schema():
    #         _str += getattr(self, col_name)
    #         _str += ","
    #     if append_newline:
    #         _str += "\n"
    #     return _str
