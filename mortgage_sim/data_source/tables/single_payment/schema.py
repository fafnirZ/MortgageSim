from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class SinglePaymentsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "name": pl.String(),  # canonical id attached to a recurring event.
            "date": pl.Date(),
            "amount": pl.Float64(),
        }
