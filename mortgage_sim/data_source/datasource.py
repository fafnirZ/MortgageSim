from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from mortgage_sim.data_source.signatures import DataSourceSignature
from mortgage_sim.data_source.tables.events.table import EventsTable
from mortgage_sim.data_source.tables.loan_parameters.table import LoanParametersTable
from mortgage_sim.data_source.tables.recurring_payments.table import (
    RecurringPaymentsTable,
)
from mortgage_sim.data_source.tables.single_payments.table import SinglePaymentsTable
from mortgage_sim.data_source.tables.templates.table import TableTemplate
from mortgage_sim.utils.asserts import assert_type


@dataclass(frozen=True)
class DataSource:
    path: Path
    signature: ClassVar[type[DataSourceSignature]] = DataSourceSignature

    @classmethod
    def init(cls, *, path: Path):
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
        cls.signature.assert_path_endswith_signature(path)

        # create datasource
        path.mkdir()

        # create all tables
        all_tables = [
            EventsTable,
            RecurringPaymentsTable,
            SinglePaymentsTable,
            LoanParametersTable,
        ]

        for table_class in all_tables:
            # create events table
            _table_class: type[TableTemplate] = table_class
            _table_class.create(
                path=path / _table_class.get_signature().get_signature()
            )

    @classmethod
    def from_path(cls, *, path: Path):
        assert_type(path, Path)

        cls.signature.assert_path_endswith_signature(path)

        if not path.is_dir():
            raise FileNotFoundError(
                f"Datasource cannot be instantiated at path: {path}"
                "It either does not exist or is not a directory"
            )
        return cls(path=path)

    #
    # instance methods
    #

    @property
    def events_table(self):
        return EventsTable(path=self.path / EventsTable.get_signature().get_signature())

    @property
    def recurring_payments_table(self):
        return RecurringPaymentsTable(
            path=self.path / RecurringPaymentsTable.get_signature().get_signature()
        )

    @property
    def single_payments_table(self):
        return SinglePaymentsTable(
            path=self.path / SinglePaymentsTable.get_signature().get_signature()
        )

    @property
    def loan_parameters_table(self):
        return LoanParametersTable(
            path=self.path / LoanParametersTable.get_signature().get_signature()
        )
