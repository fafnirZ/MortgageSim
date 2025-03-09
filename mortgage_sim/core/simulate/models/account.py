from dataclasses import dataclass

from mortgage_sim.utils.asserts import assert_type


@dataclass
class Account:
    balance: float

    def __post_init__(self):
        assert_type(self.balance, float)


class LoanAccount(Account): ...


class OffsetAccount(Account): ...
