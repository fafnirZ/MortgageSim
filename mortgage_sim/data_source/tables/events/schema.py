from datetime import datetime
from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class EventsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "fk__recurring_payments": pl.String(),
            "fk__single_payments": pl.String(),
            "fk__loan_parameters": pl.String(),
            # metadata
            "event_registered_timestamp": pl.Datetime(),
        }

    @classmethod
    def get_python_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": str,
            "fk__recurring_payments": (str, None),
            "fk__single_payments": (str, None),
            "fk__loan_parameters": (str, None),
            # metadata
            "event_registered_timestamp": datetime,
        }
