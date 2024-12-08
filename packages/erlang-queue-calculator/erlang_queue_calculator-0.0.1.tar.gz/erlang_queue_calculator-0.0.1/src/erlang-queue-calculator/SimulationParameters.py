from src.AxisToModify import AxisToModify
from src.DesiredSimulationOutcome import DesiredSimulationOutcome
from src.MMCKParameters import MMCKParameters


class SimulationParameters:
    def __init__(self, starting_parameters: MMCKParameters, axis_to_modify: AxisToModify, desired_simulation_outcome: DesiredSimulationOutcome):
        self.starting_parameters = starting_parameters
        self.axis_to_modify = axis_to_modify
        self.desired_simulation_outcome = desired_simulation_outcome