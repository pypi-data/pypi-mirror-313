import math
from math import factorial

from src.MMCKPerformance import MMCKPerformance

def calculate_m_m_c_k_performance(arrival_rate: float, service_rate: float, number_of_servers: int, size_of_queue: int) -> MMCKPerformance:
    """
    The most important value we required is p0.
    This is the probability that there are no customers in the system. We calculate that by figuring out
    - the probability of having between 0 and (number_of_servers - 1)
    - the probability of having number_of_servers or more up to (number_of_servers + size_of_queue)

    p0 is the inverse of the sum of these probabilities.
    """

    offered_load = arrival_rate / service_rate
    rho = offered_load / number_of_servers

    p0 = None
    if rho == 1:
        p0 = get_po_when_rho_is_one(offered_load, number_of_servers, size_of_queue)
    else:
        probability_of_between_zero_and_c_minus_one_customers = get_probability_of_between_zero_and_c_minus_one_customers(arrival_rate, service_rate,
                                                                              number_of_servers)
        probability_of_c_or_more_customers = get_probability_of_c_or_more_customers(arrival_rate, service_rate, number_of_servers, size_of_queue)
        p0 = 1.0 / (probability_of_between_zero_and_c_minus_one_customers + probability_of_c_or_more_customers)

    """
    We use p0 to calculate each of the other pN values - the probability
    of there being N customers in the system.
    """
    p_n_values = calculate_p_n_values(p0, arrival_rate, service_rate, number_of_servers, size_of_queue)

    average_number_of_customers_in_the_queue = get_average_number_of_customers_in_the_queue(number_of_servers, size_of_queue, p_n_values)
    average_number_of_customers_in_the_system = get_average_number_of_customers_in_the_system(number_of_servers, size_of_queue, p_n_values)

    effective_arrival_rate = calculate_effective_arrival_rate(arrival_rate, number_of_servers, size_of_queue, p_n_values)

    """
    These calculations are done using Little's Law.
    
    The relationship between the time in the queue/system can be calculated by
    contrasting the number of customers in them and the effective arrival rate.
    """
    average_wait_in_the_queue = average_number_of_customers_in_the_queue / effective_arrival_rate
    average_wait_in_the_system = average_number_of_customers_in_the_system / effective_arrival_rate

    return MMCKPerformance(
        arrival_rate,
        service_rate,
        number_of_servers,
        size_of_queue,
        average_number_of_customers_in_the_queue,
        average_number_of_customers_in_the_system,
        average_wait_in_the_queue,
        average_wait_in_the_system,
        p_n_values[number_of_servers + size_of_queue],
        p_n_values
    )

def calculate_probability_of_loss_erlang_b(arrival_rate: float, service_rate: float, number_of_servers: int) -> float:
    offered_load = arrival_rate / service_rate
    numerator = math.pow(offered_load, number_of_servers) / factorial(number_of_servers)
    denominator = 0

    for i in inclusive_range(0, number_of_servers):
        denominator += math.pow(offered_load, i) / factorial(i)

    return numerator / denominator

def calculate_probability_of_blocking_erlang_c(arrival_rate: float, service_rate: float, number_of_servers: int) -> float:
    offered_load = arrival_rate / service_rate

    numerator = (math.pow(offered_load, number_of_servers) / factorial(number_of_servers) * (number_of_servers / (number_of_servers * offered_load)))
    denominator = 0

    for i in inclusive_range(0, number_of_servers - 1):
        denominator += math.pow(offered_load, i) / factorial(i)

    denominator += numerator

    return numerator / denominator

def calculate_p_n_values(p0: float, arrival_rate: float, service_rate: float, number_of_servers: int, size_of_queue: int) -> dict[int, float]:
    result = {
        0: p0
    }

    for i in inclusive_range(1, number_of_servers + size_of_queue):
        result[i] = calculate_p_n(p0, arrival_rate, service_rate, number_of_servers, size_of_queue, i)

    return result

def calculate_p_n(p0: float, arrival_rate: float, service_rate: float, c: int, k: int, n: int) -> float:
    offered_load = arrival_rate / service_rate
    rho = offered_load / c
    if rho == 1:
        if n < c:
            return (math.pow(c, n) / factorial(n)) * p0
        else:
            return (math.pow(c, c) / factorial(c)) * p0
    else:
        if n < c:
            return (math.pow(offered_load, n) / factorial(n)) * p0
        elif n > (c + k):
            return 0
        else:
            return (math.pow(offered_load, n) / (factorial(c) * (math.pow(c, n - c)))) * p0

def get_probability_of_between_zero_and_c_minus_one_customers(arrival_rate: float, service_rate: float, c: int) -> float:
    offered_load = arrival_rate / service_rate
    result = 0

    for n in inclusive_range(0, c - 1):
        result += (math.pow(offered_load, n) / factorial(n))

    return result

def get_probability_of_c_or_more_customers(arrival_rate: float, service_rate: float, c: int, size_of_queue: int) -> float:
    k = c + size_of_queue
    offered_load = arrival_rate / service_rate
    all_servers_are_busy = math.pow(offered_load, c) / factorial(c)

    numerator_for_between_c_and_k_customers = (1 - (math.pow((offered_load / c), (k - c + 1))))
    denominator_for_between_c_and_k_customers = (1 - (offered_load / c))

    return all_servers_are_busy * (numerator_for_between_c_and_k_customers / denominator_for_between_c_and_k_customers)

def get_po_when_rho_is_one(offered_load: float, c: int, k: int) -> float:
    capacity = c + k
    denominator = 0

    for n in inclusive_range(0, c - 1):
        denominator += math.pow(offered_load, n) / factorial(n)

    denominator += ( math.pow(offered_load, c) / factorial(c)) * (1 + capacity - c)

    return 1 / denominator

"""
This calculates the average number of customers in the queue.

This is obtained by summing the expected number of customers in the queue
in all the states where we have more customers than servers.
"""
def get_average_number_of_customers_in_the_queue(c: int, k: int, p_n_values: dict[int, float]) -> float:
    result = 0

    for n in inclusive_range(c, c + k):
        result += ((n - c) * p_n_values[n])

    return result

"""
This calculates the average number of customers in the system.

This is obtained by summing the various values of expected number of customers
multiplied by their expected probabilities of occurring.
 """
def get_average_number_of_customers_in_the_system(c: int, k: int, p_n_values: dict[int, float]) -> float:
    result = 0

    for n in inclusive_range(0, c + k):
        result += (n * p_n_values[n])

    return result

"""
This returns the effective arrival rate.

This is the arrival rate multiplied by the probability that
we are not currently blocked - this is 1 minus the probability that we
are currently being blocked. We are being blocked if there are exactly
c + k customers in the system.
"""
def calculate_effective_arrival_rate(arrival_rate: float, c: int, k: int, p_n_values: dict[int, float]) -> float:
    return arrival_rate * (1 - p_n_values[c + k])

def inclusive_range(start, end) -> range:
    return range(start, end + 1)