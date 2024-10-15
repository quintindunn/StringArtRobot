class InvalidDirectionException(BaseException):
    def __init__(self, direction: int):
        self.direction = direction

    def __str__(self):
        return f"Direction {self.direction} is not a recognized direction!"

    __repr__ = __str__
