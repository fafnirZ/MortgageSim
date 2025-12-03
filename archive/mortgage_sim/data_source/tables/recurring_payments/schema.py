from datetime import date
from enum import Enum as PYEnum
from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class RecurringPaymentsType(PYEnum):
    RECURRING_START = "RECURRING_START"
    RECURRING_END = "RECURRING_END"


class FrequencyType(PYEnum):
    WEEKLY = "WEEKLY"
    FORTNIGHTLY = "FORTNIGHTLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class RecurringPaymentsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "name": pl.String(),  # canonical id attached to a recurring event.
            "date": pl.Date(),
            "type": pl.Enum(["RECURRING_START", "RECURRING_END"]),
            "amount": pl.Float64(),
            "frequency": pl.Enum(
                [
                    "WEEKLY",
                    "FORTNIGHTLY",
                    "MONTHLY",
                    "YEARLY",
                ]
            ),
        }

    @classmethod
    def get_python_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": str,
            "name": str,  # canonical id attached to a recurring event.
            "date": date,
            "type": RecurringPaymentsType,
            "amount": (float, type(None)),
            "frequency": (FrequencyType, type(None)),
        }
