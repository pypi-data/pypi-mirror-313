from enum import Enum

class PerformanceCharacteristics(Enum):
    AverageWaitInSystem = 0
    AverageWaitInQueue = 1
    AverageNumberOfCustomersInSystem = 2
    AverageNumberOfCustomersInQueue = 3
    ProbabilityOfBlocking = 4