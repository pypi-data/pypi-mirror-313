from src.PerformanceCharacteristics import PerformanceCharacteristics

class DesiredSimulationOutcome:
    def __init__(self, performance_characteristic: PerformanceCharacteristics, value: float):
        self.performance_characteristic = performance_characteristic
        self.value = value