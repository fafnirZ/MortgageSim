from abc import ABC, abstractmethod
from pathlib import Path
import re

from mortgage_sim.utils.asserts import assert_type


class SignatureError(Exception): ...


class SignatureTemplate(ABC):
    @abstractmethod
    def get_signature():
        raise NotImplementedError

    @abstractmethod
    def get_regex_signature():
        raise NotImplementedError

    @classmethod
    def path_contains_signature(cls, path: Path) -> bool:
        assert_type(path, Path)
        return re.match(str(path), cls.get_regex_signature())

    @classmethod
    def assert_path_endswith_signature(cls, path: Path):
        assert_type(path, Path)
        leaf = path.name
        if not re.match(cls.get_regex_signature(), str(leaf)):
            raise SignatureError(
                f"path: {path} does not end with {cls.get_regex_signature()}"
            )


class DataSourceSignature(SignatureTemplate):
    def get_signature():
        return "datasource"

    def get_regex_signature():
        return r"datasource"


class EventsTableSignature(SignatureTemplate):
    def get_signature():
        return "events.parquet"

    def get_regex_signature():
        return r"events\.parquet"


class RecurringPaymentsTableSignature(SignatureTemplate):
    def get_signature():
        return "recurring_payments.parquet"

    def get_regex_signature():
        return r"recurring_payments\.parquet"


class SinglePaymentsTableSignature(SignatureTemplate):
    def get_signature():
        return "single_payments.parquet"

    def get_regex_signature():
        return r"single_payments\.parquet"


class LoanParametersTableSignature(SignatureTemplate):
    def get_signature():
        return "loan_parameters.parquet"

    def get_regex_signature():
        return r"loan_parameters\.parquet"
