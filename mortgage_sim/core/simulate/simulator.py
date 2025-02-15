from dataclasses import dataclass
from mortgage_sim.core.simulate.simulator_utils import SimulatorUtils
from mortgage_sim.data_source.datasource import DataSource


@dataclass
class Simulator(SimulatorUtils):
    data_source: DataSource

    def get_datasource(self):
        return self.data_source
