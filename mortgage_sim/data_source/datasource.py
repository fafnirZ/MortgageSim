from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class DataSource:
    path: Path

    @classmethod
    def create(cls, *, path: Path):
        assert_type(path, Path)
        if path.exists():
            raise FileExistsError(
                f"Datasource cannot be created at path: {path}"
                "since something already exists there"
            )

        # init data_source
        cls.__init_datasource(path=path)

        return cls(path=path)

    @classmethod
    def __init_datasource(cls, *, path: Path):
        # assert ends with datasource signature
        path.mkdir()

    @classmethod
    def from_path(cls, *, path: Path):
        assert_type(path, Path)
        if not path.is_dir():
            raise FileNotFoundError(
                f"Datasource cannot be instantiated at path: {path}"
                "It either does not exist or is not a directory"
            )
        return cls(path=path)
