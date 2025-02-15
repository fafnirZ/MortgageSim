from __future__ import annotations
from abc import abstractmethod
from typing import Optional
from datetime import date as Date_, datetime
from uuid import uuid4

from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.tables.events.record import EventsTableRecord
from mortgage_sim.data_source.tables.single_payments.record import (
    SinglePaymentsTableRecord,
)

from mortgage_sim.utils.asserts import assert_type
import polars as pl


class SinglePaymentEventCreator:
    @abstractmethod
    def get_datasource(self) -> DataSource:
        raise NotImplementedError

    def new_single_payment_event(
        self,
        name: str,
        date: Date_,
        amount: float,
    ):
        assert_type(name, str)
        assert_type(date, Date_)
        assert_type(amount, float)

        events_uuid = str(uuid4())
        single_payment_uuid = str(uuid4())

        # init events record
        events_record = EventsTableRecord(
            uuid=events_uuid,
            fk__recurring_payments=None,
            fk__single_payments=single_payment_uuid,
            fk__loan_parameters=None,
            event_registered_timestamp=datetime.now(),
        )

        singlep_record = SinglePaymentsTableRecord(
            uuid=single_payment_uuid,
            name=name,
            date=date,
            amount=amount,
        )
