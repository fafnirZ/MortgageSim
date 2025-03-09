from dataclasses import dataclass

from mortgage_sim.utils.asserts import assert_type


@dataclass
class Account:
    id: str
    balance: float

    def __post_init__(self):
        assert_type(self.balance, float)


class LoanAccount(Account): 
    id = "loan_account"


class OffsetAccount(Account):
    id = "offset_account"
