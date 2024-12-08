from typing import Optional, TypeVar, Generic

R = TypeVar('R')

class Result(Generic[R]):
    def __init__(self, result: Optional[R], error: Optional[BaseException]):
        self.result = result
        self.error = error

    def is_success(self):
        return self.result is not None

    def is_failure(self):
        return self.error is not None

    def unwrap(self):
        if self.is_success():
            return self.result
        else:
            raise self.error

    @staticmethod
    def success(result):
        return Result(result, None)

    @staticmethod
    def failure(error):
        return Result(None, error)

