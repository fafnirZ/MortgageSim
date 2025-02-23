import pytest
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.signatures import DataSourceSignature, SignatureError


def test_datasource_creation(tmp_path):
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.init(path=p)

    assert ds.path.exists()
    assert ds.events_table.path.exists()
    assert ds.recurring_payments_table.path.exists()
    assert ds.single_payments_table.path.exists()
    assert ds.loan_parameters_table.path.exists()


def test_datasource_instantiation(tmp_path):
    p = tmp_path / DataSourceSignature.get_signature()
    DataSource.init(path=p)
    ds = DataSource.from_path(path=p)
    assert ds.path.is_dir()


def test_datasource_creation_not_signature(tmp_path):
    p = tmp_path / "notdatasource"
    with pytest.raises(SignatureError):
        DataSource.init(path=p)
