from src import DesiredSimulationOutcome
from src.AxisToModify import AxisToModify
from src.MMCKParameters import MMCKParameters
from src.MMCKPerformance import MMCKPerformance
from src.PerformanceCharacteristics import PerformanceCharacteristics
from src.InputParameter import InputParameter
from src.Result import Result
from src.SimulationParameters import SimulationParameters
from src.erlang import calculate_m_m_c_k_performance

def simulate(parameters: SimulationParameters) -> Result[MMCKPerformance]:
    m_m_c_k_parameters = parameters.starting_parameters
    axis_to_modify = parameters.axis_to_modify

    performance = calculate_m_m_c_k_performance(m_m_c_k_parameters.arrival_rate, m_m_c_k_parameters.service_rate,
                                                m_m_c_k_parameters.number_of_servers,
                                                m_m_c_k_parameters.size_of_queue)

    if satisfies_desired_outcome(performance, parameters.desired_simulation_outcome):
        return Result.success(performance)

    while not axis_to_modify_has_reached_maximum_value(m_m_c_k_parameters, axis_to_modify):
        m_m_c_k_parameters = modify_input_parameters(m_m_c_k_parameters, axis_to_modify)
        performance = calculate_m_m_c_k_performance(m_m_c_k_parameters.arrival_rate, m_m_c_k_parameters.service_rate,
                                                    m_m_c_k_parameters.number_of_servers,
                                                    m_m_c_k_parameters.size_of_queue)

        if satisfies_desired_outcome(performance, parameters.desired_simulation_outcome):
            return Result.success(performance)

    return Result.failure(Exception("Cannot meet criteria"))

def modify_input_parameters(parameters: MMCKParameters, axis_to_modify: AxisToModify):
    if axis_to_modify.axis == InputParameter.InterArrivalTime:
        parameters.arrival_rate += axis_to_modify.step
    elif axis_to_modify.axis == InputParameter.InterServiceTime:
        parameters.service_rate += axis_to_modify.step
    elif axis_to_modify.axis == InputParameter.NumberOfServers:
        parameters.number_of_servers += axis_to_modify.step
    elif axis_to_modify.axis == InputParameter.SizeOfQueue:
        parameters.size_of_queue += axis_to_modify.step

    return parameters

def axis_to_modify_has_reached_maximum_value(parameters: MMCKParameters, axis_to_modify: AxisToModify):
    if axis_to_modify.axis == InputParameter.InterArrivalTime:
        return parameters.arrival_rate >= axis_to_modify.maximum_value
    elif axis_to_modify.axis == InputParameter.InterServiceTime:
        return parameters.service_rate >= axis_to_modify.maximum_value
    elif axis_to_modify.axis == InputParameter.NumberOfServers:
        return parameters.number_of_servers >= axis_to_modify.maximum_value
    elif axis_to_modify.axis == InputParameter.SizeOfQueue:
        return parameters.size_of_queue >= axis_to_modify.maximum_value

def satisfies_desired_outcome(performance: MMCKPerformance, desired_simulation_outcome: DesiredSimulationOutcome):
    if desired_simulation_outcome.performance_characteristic == PerformanceCharacteristics.AverageWaitInSystem:
        return performance.average_wait_in_system <= desired_simulation_outcome.value
    elif desired_simulation_outcome.performance_characteristic == PerformanceCharacteristics.AverageWaitInQueue:
        return performance.average_wait_in_queue <= desired_simulation_outcome.value
    elif desired_simulation_outcome.performance_characteristic == PerformanceCharacteristics.AverageNumberOfCustomersInSystem:
        return performance.average_number_customers_in_the_system <= desired_simulation_outcome.value
    elif desired_simulation_outcome.performance_characteristic == PerformanceCharacteristics.AverageNumberOfCustomersInQueue:
        return performance.average_number_customers_in_the_queue <= desired_simulation_outcome.value
    elif desired_simulation_outcome.performance_characteristic == PerformanceCharacteristics.ProbabilityOfBlocking:
        return performance.probability_of_blocking <= desired_simulation_outcome.value