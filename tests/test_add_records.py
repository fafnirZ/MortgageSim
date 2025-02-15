from datetime import date
from pathlib import Path
from mortgage_sim.core.management.management import EventManager
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.signatures import DataSourceSignature


def test_add_recurring_record_single(tmp_path):
    # p = Path.cwd() / DataSourceSignature.get_signature()
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)
    em.new_recurring_payment_event(
        name="monthly_payments",
        date=date(2024, 1, 1),
        amount=1000.0,
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
        {"name": "monthly_payments", "date": date(2024, 1, 1), "amount": 1000.0},
        {"name": "monthly_payments", "date": date(2024, 2, 1), "amount": 1000.0},
        {"name": "monthly_payments", "date": date(2024, 3, 1), "amount": 1000.0},
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
