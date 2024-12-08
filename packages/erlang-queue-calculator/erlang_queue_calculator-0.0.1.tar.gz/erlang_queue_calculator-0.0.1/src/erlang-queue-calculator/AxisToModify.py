from src.InputParameter import InputParameter


class AxisToModify:
    def __init__(self, axis: InputParameter, step: int, maximum_value: int):
        self.axis = axis
        self.step = step
        self.maximum_value = maximum_value