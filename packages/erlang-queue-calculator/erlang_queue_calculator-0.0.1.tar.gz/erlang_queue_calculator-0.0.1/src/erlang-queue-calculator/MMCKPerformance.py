class MMCKPerformance:
    def __init__(self,
                 arrival_rate: float,
                 service_rate: float,
                 number_of_servers: int,
                 size_of_queue: int,
                 average_number_of_customers_in_the_queue: float,
                 average_number_of_customers_in_the_system: float,
                 average_wait_in_queue: float,
                 average_wait_in_system: float,
                 probability_of_blocking: float,
                 probability_of_n_customers: dict[int, float]):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.number_of_servers = number_of_servers
        self.size_of_queue = size_of_queue

        self.inter_arrival_time = 1 / arrival_rate
        self.inter_service_time = 1 / service_rate
        self.rho = arrival_rate / service_rate

        self.average_number_customers_in_the_queue = average_number_of_customers_in_the_queue
        self.average_number_customers_in_the_system = average_number_of_customers_in_the_system
        self.average_wait_in_queue = average_wait_in_queue
        self.average_wait_in_system = average_wait_in_system
        self.probability_of_blocking = probability_of_blocking
        self.probability_of_n_customers = probability_of_n_customers