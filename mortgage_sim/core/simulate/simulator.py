from dataclasses import dataclass
from mortgage_sim.core.simulate.simulator_utils import SimulatorUtils
from mortgage_sim.data_source.datasource import DataSource


@dataclass
class Simulator(SimulatorUtils):
    data_source: DataSource

    def get_datasource(self):
        return self.data_source

    def _prepare_simulate(self):
        # setup account based on simulator config.

        # assert loan params table has at least 1 record

        # create special record for recurring records
        # where this record has start and end date

        pass

    def simulate(self):
        """
        while rolling_loan_balance > 0:
           for all recurring payments
              if recurring payment < end_date or end_date is None
                 perform_recurring payment on accounts
           for all single payments
              if current_range contains single payment date
                 perform single payment on accounts
        """
        pass
