from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class RecurringPaymentsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "name": pl.String(),  # canonical id attached to a recurring event.
            "date": pl.Date(),
            "type": pl.Enum(["RECURRING_START", "RECURRING_END"]),
            "amount": pl.Float64(),
        }
