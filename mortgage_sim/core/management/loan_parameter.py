from abc import abstractmethod
from typing import Optional

from mortgage_sim.data_source.datasource import DataSource


class LoanParameterEventCreator:
    @abstractmethod
    def get_datasource(self) -> DataSource:
        raise NotImplementedError

    def new_loan_parameter(
        self,
        *,
        principle_amount: Optional[float],
        interest_rate: Optional[float],
        monthly_repayment: Optional[float],
    ):
        # can update:
        # principle NO
        # interest_rate yes
        # monthly_repayments yes

        pass
