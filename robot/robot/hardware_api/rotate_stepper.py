from .. import instructions

BASE_STEPS_PER_REVOLUTION = 200
MICRO_STEPS = 64

STP_P_REV = BASE_STEPS_PER_REVOLUTION * MICRO_STEPS
STP_P_DEG = 360 / STP_P_REV


def move_degrees(degrees: int, direction: int):
    if direction == instructions.Direction.CW:
        pass
