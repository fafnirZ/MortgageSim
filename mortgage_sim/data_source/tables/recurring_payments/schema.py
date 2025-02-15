from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class RecurringPaymentsTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "id": pl.String(),
        }
