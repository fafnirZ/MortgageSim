from abc import abstractmethod
from datetime import datetime
from typing import Optional
from uuid import uuid4

from mortgage_sim.core.management.errors import EventCreationError
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.tables.events.record import EventsTableRecord
from mortgage_sim.data_source.tables.loan_parameters.record import (
    LoanParametersTableRecord,
)
from mortgage_sim.utils.asserts import assert_type
import polars as pl


class LoanParameterEventCreator:
    @abstractmethod
    def get_datasource(self) -> DataSource:
        raise NotImplementedError

    def __take_principle_amount_from_previous_value(self, *, df: pl.DataFrame) -> float:
        existing_principle_amount = set(df["principle_amount"].to_list())
        if len(existing_principle_amount) > 1:
            raise EventCreationError(
                "LoanParameter is corrupted\n",
                "Principle amount has been changed...",
            )

        return existing_principle_amount[0]

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

        df = (
            self
            .get_datasource()
            .loan_parameters_table
            .scan_csv()
            .collect()
        )  # fmt: off

        #
        # validations
        #
        if len(df) == 0:
            # initially everything else must be set
            assert_type(principle_amount, float)
            assert_type(interest_rate, float)
            assert_type(monthly_repayment, float)
        else:
            assert_type(principle_amount, type(None))  # must be none

        # if set to none
        # its not a new loan parameter workflow
        if principle_amount is None:
            principle_amount = self.__take_principle_amount_from_previous_value(df=df)

        events_uuid = str(uuid4())
        loan_parameter_uuid = str(uuid4())

        # init events record
        events_record = EventsTableRecord(
            uuid=events_uuid,
            fk__recurring_payments=None,
            fk__single_payments=None,
            fk__loan_parameters=loan_parameter_uuid,
            event_registered_timestamp=datetime.now(),
        )

        loan_parameter_record = LoanParametersTableRecord(
            uuid=loan_parameter_uuid,
            principle_amount=principle_amount,
            interest_rate=interest_rate,
            monthly_repayment=monthly_repayment,
        )

        # append to events table
        (self
            .get_datasource()
            .events_table
            .append_record(record=events_record))  # fmt: off

        # append to loan parameter table
        (self
            .get_datasource()
            .loan_parameters_table
            .append_record(record=loan_parameter_record))  # fmt: off
