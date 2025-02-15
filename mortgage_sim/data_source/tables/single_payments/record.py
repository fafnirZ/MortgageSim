from mortgage_sim.data_source.tables.single_payments.schema import (
    SinglePaymentsTableSchema,
)
from mortgage_sim.data_source.tables.templates.record import RecordTemplate


class SinglePaymentsTableRecord(RecordTemplate):
    @classmethod
    def get_schema(cls) -> type[SinglePaymentsTableSchema]:
        return SinglePaymentsTableSchema
