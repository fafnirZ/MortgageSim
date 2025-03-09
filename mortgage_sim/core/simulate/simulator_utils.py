from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Generator
from dateutil.relativedelta import relativedelta

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

    @classmethod
    def get_next_period(
        cls, *, data_source: DataSource
    ) -> Generator[tuple[date, date], Any, Any]:
        """Returns a generator which yields time periods."""
        assert_type(data_source, DataSource)
        loan_parameters_table_lf = (
            data_source
            .loan_parameters_table
            .scan_csv()
        )  # fmt: off

        repayment_start_date = (
            loan_parameters_table_lf["monthly_repayment_start_date"]
            .collect()
            .to_list()[0]
        )  # fmt: off

        period_start_date = repayment_start_date
        while True:
            start_of_period = period_start_date + 1
            end_of_period = period_start_date + relativedelta(months=1)
            yield (start_of_period, end_of_period)

    @classmethod
    def date_in_period(
        cls,
        *,
        date: date,
        period: tuple[date, date],
    ):
        """Is given Date within a provided period?"""
        if period[0] <= date <= period[1]:
            return True
        return False
