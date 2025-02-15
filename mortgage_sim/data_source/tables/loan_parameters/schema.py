from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class LoanParametersTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "principle_amount": pl.Float32(),
            "interest_rate": pl.Float32(),  # range(0,100) i.e. not a decimal
            "monthly_repayments": pl.Float32(),
            "update_date": pl.Date(),
        }
