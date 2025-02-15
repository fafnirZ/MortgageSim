from mortgage_sim.data_source.tables.loan_parameters.schema import (
    LoanParametersTableSchema,
)
from mortgage_sim.data_source.tables.templates.record import RecordTemplate


class LoanParametersTableRecord(RecordTemplate):
    @classmethod
    def get_schema(cls) -> type[LoanParametersTableSchema]:
        return LoanParametersTableSchema
