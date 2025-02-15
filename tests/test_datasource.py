import pytest
from mortgage_sim.data_source.datasource import DataSource
from mortgage_sim.data_source.signatures import DataSourceSignature, SignatureError


def test_datasource_creation(tmp_path):
    p = tmp_path / DataSourceSignature.get_signature()
    ds = DataSource.create(path=p)
    assert ds.path.exists()


def test_datasource_instantiation(tmp_path):
    p = tmp_path / DataSourceSignature.get_signature()
    DataSource.create(path=p)
    ds = DataSource.from_path(path=p)
    assert ds.path.is_dir()


def test_datasource_creation_not_signature(tmp_path):
    p = tmp_path / "notdatasource"
    with pytest.raises(SignatureError):
        DataSource.create(path=p)
