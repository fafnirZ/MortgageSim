from mortgage_sim.data_source.datasource import DataSource


def test_datasource_creation(tmp_path):
    ds = DataSource.create(path=tmp_path / "datasource")
    assert ds.path.exists()
