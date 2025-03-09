from dataclasses import dataclass
from datetime import date
from mortgage_sim.core.simulate.models.account import LoanAccount, OffsetAccount
from mortgage_sim.core.simulate.simulator_utils import SimulatorUtils
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.tables.single_payments.record import (
    SinglePaymentsTableRecord,
)


@dataclass
class Simulator(SimulatorUtils):
    data_source: DataSource

    def get_datasource(self):
        return self.data_source

    def _prepare_simulate(self):
        # assert loan params table has at least 1 record
        initial_loan_params = (
            self
            .data_source
            .loan_parameters_table
            .scan_csv()
            .collect()
            .row(0, named=True)
        )  # fmt: off
        # setup account based on simulator config.
        self.loan_account = LoanAccount(
            balance=initial_loan_params["principle_amount"],
        )
        self.offset_account = OffsetAccount(
            balance=0,
        )

        # create special record for recurring records
        # where this record has start and end date

        pass

    def simulate(self):
        """
        while rolling_loan_balance > 0:
           for all recurring payments
              if recurring payment < end_date or end_date is None
                 perform_recurring payment on accounts
           for all single payments
              if current_range contains single payment date
                 perform single payment on accounts
        """
        for period in self.get_next_period():
            # exit condition
            if self.loan_account.balance <= 0:
                break
            period_start = period[0]
            period_end = period[1]

            self.__apply_single_payments(period)

    def __apply_single_payments(self, period: tuple[date, date]):
        """Apply single payments"""
        # NOTE non performant
        single_payments_df = (
            self
            .data_source
            .single_payments_table
            .scan_csv()
            .collect()
        )  # fmt: off

        for record in single_payments_df.rows(named=True):
            record_obj = SinglePaymentsTableRecord(**record)
            date = record_obj.date
            if self.date_in_period(date=date, period=period):
                self.offset_account += record_obj.amount
