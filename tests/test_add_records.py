from datetime import date
from pathlib import Path

import pytest
from mortgage_sim.core.management.management import EventManager
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.signatures import DataSourceSignature
from mortgage_sim.data_source.tables.recurring_payments.schema import FrequencyType


def test_add_recurring_record_single(tmp_path):
    # p = Path.cwd() / DataSourceSignature.get_signature()
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)
    em.new_recurring_payment_event(
        name="monthly_payments",
        date=date(2024, 1, 1),
        amount=1000.0,
        frequency=FrequencyType.MONTHLY,
    )

    events_df = ds.events_table.scan_csv().collect()
    assert len(events_df) == 1
    recurring_df = ds.recurring_payments_table.scan_csv().collect()
    assert len(recurring_df) == 1


def test_add_recurring_record_multiple_records(tmp_path):
    # p = Path.cwd() / DataSourceSignature.get_signature()
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)

    records = [
        {
            "name": "monthly_payments",
            "date": date(2024, 1, 1),
            "amount": 1000.0,
            "frequency": FrequencyType.MONTHLY,
        },
        {
            "name": "monthly_payments",
            "date": date(2024, 2, 1),
            "amount": 1000.0,
            "frequency": FrequencyType.MONTHLY,
        },
        {
            "name": "monthly_payments",
            "date": date(2024, 3, 1),
            "amount": 1000.0,
            "frequency": FrequencyType.MONTHLY,
        },
    ]

    for record in records:
        em.new_recurring_payment_event(**record)

    events_df = ds.events_table.scan_csv().collect()
    assert len(events_df) == 3
    recurring_df = ds.recurring_payments_table.scan_csv().collect()
    assert len(recurring_df) == 3

    assert recurring_df["type"].to_list() == [
        "RECURRING_START",
        "RECURRING_END",
        "RECURRING_START",
    ]


#
# single records
#
def test_add_single_record_multiple_of_them(tmp_path):
    # p = Path.cwd() / DataSourceSignature.get_signature()
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)

    records = [
        {"name": "monthly_payments", "date": date(2024, 1, 1), "amount": 1000.0},
        {"name": "monthly_payments", "date": date(2024, 2, 1), "amount": 1000.0},
        {"name": "monthly_payments", "date": date(2024, 3, 1), "amount": 1000.0},
    ]

    for record in records:
        em.new_single_payment_event(**record)

    events_df = ds.events_table.scan_csv().collect()
    assert len(events_df) == 3
    recurring_df = ds.single_payments_table.scan_csv().collect()
    assert len(recurring_df) == 3


#
# loan parameters
#


# fmt: off
@pytest.mark.parametrize(
    "records",
    [
        [
            {"principle_amount": 300000.0, "interest_rate": 6.8, "monthly_repayment": 2600.0},
        ],
        [
            {"principle_amount": 300000.0, "interest_rate": 6.8, "monthly_repayment": 2600.0},
            {"principle_amount": None, "interest_rate": 6.0, "monthly_repayment": 2300.0},
            {"principle_amount": None, "interest_rate": 5.3, "monthly_repayment": 2000.0},
        ],
        pytest.param([
            {"principle_amount": 300000.0, "interest_rate": 6.8, "monthly_repayment": 2600.0},
            {"principle_amount": 300000.0, "interest_rate": 6.0, "monthly_repayment": 2300.0},
            {"principle_amount": 300000.0, "interest_rate": 5.3, "monthly_repayment": 2000.0},
        ], marks=pytest.mark.xfail), # expected to fail
    ]
)
def test_add_loan_parameter_records(tmp_path, records):
    # p = Path.cwd() / DataSourceSignature.get_signature()
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)


    for record in records:
        em.new_loan_parameter(**record)

    events_df = ds.events_table.scan_csv().collect()
    assert len(events_df) == len(records)
    loan_params_df = ds.loan_parameters_table.scan_csv().collect()
    assert len(loan_params_df) == len(records)
# fmt: on
