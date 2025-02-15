from mortgage_sim.data_source.tables.recurring_payments.schema import (
    RecurringPaymentsTableSchema,
)
from mortgage_sim.data_source.tables.templates.record import RecordTemplate


class RecurringPaymentsTableRecord(RecordTemplate):
    @classmethod
    def get_schema(cls) -> type[RecurringPaymentsTableSchema]:
        return RecurringPaymentsTableSchema
