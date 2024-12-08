class MMCKParameters:
    def __init__(self, arrival_rate: float, service_rate: float, number_of_servers: int, size_of_queue: int):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.number_of_servers = number_of_servers
        self.size_of_queue = size_of_queue