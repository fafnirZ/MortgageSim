from __future__ import annotations
from abc import abstractmethod
from typing import Optional
from datetime import date as Date_, datetime
from uuid import uuid4

from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.tables.events.record import EventsTableRecord
from mortgage_sim.data_source.tables.recurring_payments.record import (
    RecurringPaymentsTableRecord,
)
from mortgage_sim.data_source.tables.recurring_payments.schema import (
    RecurringPaymentsType,
)
from mortgage_sim.utils.asserts import assert_type
import polars as pl


class RecurringPaymentEventCreator:
    @abstractmethod
    def get_datasource(self) -> DataSource:
        raise NotImplementedError

    @staticmethod
    def __determine_event_type(*, df: pl.DataFrame, name: str) -> RecurringPaymentsType:
        """
        1. If "name" record does not yet exist
            RECURRING_START
        2. If record with same "name" already exists
            if the latest record with the same "name" == "START"
                RECURRING_END
            if the latest record with the same "name" == "END"
                RECURRING_START
        """
        records_with_same_canonical_name = df.filter(pl.col("name") == name)
        # check if recurring payment of same
        # name already exists
        # based on that itll dictate next logic
        __event_type = None
        if len(records_with_same_canonical_name) > 0:
            latest_record_with_same_canonical_name = (
                df
                .sort("date", descending=True)
                .row(0, named=True)
            )  # fmt: off
            if (
                latest_record_with_same_canonical_name["type"]
                == RecurringPaymentsType.RECURRING_START.value
            ):
                __event_type = RecurringPaymentsType.RECURRING_END
            else:
                __event_type = RecurringPaymentsType.RECURRING_START

        else:
            # record does not exist yet
            __event_type = RecurringPaymentsType.RECURRING_START

        return __event_type

    def new_recurring_payment_event(
        self,
        *,
        name: str,
        date: Optional[Date_],
        amount: Optional[float],
    ):
        assert_type(name, str)
        df = (
                self
                .get_datasource()
                .recurring_payments_table
                .scan_csv()
                .collect()
            )  # fmt: off
        __event_type = self.__determine_event_type(
            df=df,
            name=name,
        )

        events_uuid = str(uuid4())
        recurring_payment_uuid = str(uuid4())

        # init events record
        events_record = EventsTableRecord(
            uuid=events_uuid,
            fk__recurring_payments=recurring_payment_uuid,
            fk__single_payments=None,
            fk__loan_parameters=None,
            event_registered_timestamp=datetime.now(),
        )

        if __event_type == RecurringPaymentsType.RECURRING_START:
            assert_type(date, Date_)
            assert_type(amount, (int, float))

        elif __event_type == RecurringPaymentsType.RECURRING_END:
            pass

        recurring_record = RecurringPaymentsTableRecord(
            uuid=recurring_payment_uuid,
            name=name,
            date=date,
            type=__event_type,
            amount=amount,
        )

        # append to events table
        (self
            .get_datasource()
            .events_table
            .append_record(record=events_record))  # fmt: off

        # append to recurring table
        (self
            .get_datasource()
            .recurring_payments_table
            .append_record(record=recurring_record))  # fmt: off
