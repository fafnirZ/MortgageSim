from datetime import date
from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class LoanParametersTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "principle_amount": pl.Float32(),
            "interest_rate": pl.Float32(),  # range(0,100) i.e. not a decimal
            "monthly_repayment": pl.Float32(),
        }

    @classmethod
    def get_python_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": str,
            "principle_amount": float,
            "interest_rate": (float, type(None)),  # range(0,100) i.e. not a decimal
            "monthly_repayment": (float, type(None)),
        }
