from datetime import date
from pathlib import Path
from mortgage_sim.core.management import EventManager
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.signatures import DataSourceSignature


def test_add_recurring_record_single(tmp_path):
    p = Path.cwd() / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    em = EventManager(data_source=ds)
    em.new_recurring_payment_event(
        name="monthly_payments",
        date=date(2024, 1, 1),
        amount=1000,
    )

    events_df = ds.events_table.scan_csv().collect()
    assert len(events_df) == 1
