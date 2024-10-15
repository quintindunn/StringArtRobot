import logging
import time

from .. import instructions

from .exceptions import InvalidDirectionException

from .config import (TBL_DIR_PIN, TBL_STP_PIN, TBL_INVERT_DIRECTION, TBL_STP_COOLDOWN_MICRO_SECONDS,
                     TBL_STP_OFF_TIME_MICRO_SECONDS)
from .write_pin import write_pin

logger = logging.getLogger("robot.hardware_api.rotate_stepper")

BASE_STEPS_PER_REVOLUTION: int = 200
MICRO_STEPS: int = 64

STP_P_REV: int = BASE_STEPS_PER_REVOLUTION * MICRO_STEPS
STP_P_DEG: float = STP_P_REV / 360
DEG_P_STEP: float = 360 / STP_P_REV


def sleep_micro_seconds(microseconds: int):
    time.sleep(microseconds/1e6)


def step():
    write_pin(TBL_STP_PIN, high=True)
    sleep_micro_seconds(TBL_STP_OFF_TIME_MICRO_SECONDS)
    write_pin(TBL_STP_PIN, high=False)


def move_tbl_degrees(angle: int):
    if not hasattr(move_tbl_degrees, "current_angle"):
        move_tbl_degrees.current_angle = 0.0

    angle_diff = (angle - move_tbl_degrees.current_angle) % 360

    if angle_diff > 180:
        steps = (360 - angle_diff) / DEG_P_STEP
        direction = instructions.Direction.CCW
    else:
        steps = angle_diff / DEG_P_STEP
        direction = instructions.Direction.CW

    if direction == instructions.Direction.CW:
        write_pin(pin=TBL_DIR_PIN, high=TBL_INVERT_DIRECTION)
    elif direction == instructions.Direction.CCW:
        write_pin(pin=TBL_DIR_PIN, high=not TBL_INVERT_DIRECTION)
    elif direction == instructions.Direction.IGNORED:
        return
    else:
        raise InvalidDirectionException(direction)

    for _ in range(round(steps)):
        step()

        if direction == instructions.Direction.CW:
            move_tbl_degrees.current_angle += DEG_P_STEP
        else:
            move_tbl_degrees.current_angle -= DEG_P_STEP

        move_tbl_degrees.current_angle %= 360
