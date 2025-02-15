from dataclasses import dataclass
from typing import Optional

from mortgage_sim.core.recurring_payment import RecurringPaymentEventCreator
from mortgage_sim.core.single_payment import SinglePaymentEventCreator
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.tables.recurring_payments.schema import (
    RecurringPaymentsType,
)
import polars as pl

from mortgage_sim.utils.asserts import assert_type


class EventCreationError(Exception): ...


@dataclass(frozen=True)
class EventManager(
    RecurringPaymentEventCreator,
    SinglePaymentEventCreator,
):
    data_source: DataSource

    def get_datasource(self) -> DataSource:
        return self.data_source

    def new_loan_parameter(
        self,
        *,
        principle_amount: Optional[float],
        interest_rate: Optional[float],
        monthly_repayment: Optional[float],
    ):
        # can update:
        # principle NO
        # interest_rate yes
        # monthly_repayments yes
        pass
