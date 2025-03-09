from datetime import date
from mortgage_sim.data_source.tables.templates.schema import SchemaTemplate
import polars as pl


class LoanParametersTableSchema(SchemaTemplate):
    @classmethod
    def get_polars_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": pl.String(),
            "interest_rate": pl.Float32(),  # range(0,100) i.e. not a decimal
            "monthly_repayment": pl.Float32(),
            "parameters_change_start_date": pl.Date(),
            # these params below should never change.
            "principle_amount": pl.Float32(),
            "monthly_repayment_start_date": pl.Date(),
            "monthly_interest_charge_start_date": pl.Date(),
            "loan_start_date": pl.Date(),
        }

    @classmethod
    def get_python_schema(self) -> dict[str, pl.DataType]:
        return {
            "uuid": str,
            "interest_rate": (float, type(None)),  # range(0,100) i.e. not a decimal
            "monthly_repayment": (float, type(None)),
            "parameters_change_start_date": date,
            # these params below should never change.
            "principle_amount": float,
            "monthly_repayment_start_date": date,  # NOTE this should never change
            "monthly_interest_charge_start_date": date,  # NOTE this should never change
            "loan_start_date": date,  # NOTE this should never change
        }
