from abc import ABC, abstractmethod

from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.utils.asserts import assert_type

DAYS_IN_YEAR = 365


class SimulatorUtils(ABC):
    @abstractmethod
    def get_datasource(self) -> DataSource:
        raise NotImplementedError

    @classmethod
    def calculate_daily_interest(
        cls,
        *,
        loan_amount: float,
        interest_rate: float,
    ) -> float:
        """
        NOTE: loan_amount is amount left in loan - offset
        NOTE: interest_rate is a value from {0,100} i.e. 6.2 etc.
        """
        assert_type(loan_amount, float)
        assert_type(interest_rate, float)
        interest_daily = interest_rate / DAYS_IN_YEAR
        interest_daily_as_decimal = interest_daily / 100
        return loan_amount * interest_daily_as_decimal
