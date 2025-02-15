from dataclasses import dataclass

from mortgage_sim.core.management.loan_parameter import LoanParameterEventCreator
from mortgage_sim.core.management.recurring_payment import RecurringPaymentEventCreator
from mortgage_sim.core.management.single_payment import SinglePaymentEventCreator
from mortgage_sim.data_source.datasource import DataSource


@dataclass(frozen=True)
class EventManager(
    RecurringPaymentEventCreator,
    SinglePaymentEventCreator,
    LoanParameterEventCreator,
):
    data_source: DataSource

    def get_datasource(self) -> DataSource:
        return self.data_source
