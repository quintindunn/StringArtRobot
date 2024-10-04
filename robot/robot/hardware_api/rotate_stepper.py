import logging
import time

from .. import instructions

from .exceptions import InvalidDirectionException

from .config import (TBL_DIR_PIN, TBL_STP_PIN, TBL_INVERT_DIRECTION, TBL_STP_COOLDOWN_MICRO_SECONDS,
                     TBL_STP_OFF_TIME_MICRO_SECONDS)
from .write_pin import write_pin

logger = logging.getLogger("robot.hardware_api.rotate_stepper")

BASE_STEPS_PER_REVOLUTION: int = 200
MICRO_STEPS: int = 66

STP_P_REV: int = BASE_STEPS_PER_REVOLUTION * MICRO_STEPS
STP_P_DEG: float = 360 / STP_P_REV

logger.debug(f"Steps/Deg: {STP_P_DEG}")


def sleep_micro_seconds(microseconds: int):
    time.sleep(microseconds/1e6)


def step():
    write_pin(TBL_STP_PIN, high=True)
    sleep_micro_seconds(TBL_STP_OFF_TIME_MICRO_SECONDS)
    write_pin(TBL_STP_PIN, high=False)


def move_tbl_degrees(degrees: int, direction: int):
    if not hasattr(move_tbl_degrees, "error"):
        move_tbl_degrees.error = 0.0

    adjusted_degrees = degrees - move_tbl_degrees.error

    target_steps = (adjusted_degrees / 360.0) * STP_P_REV

    steps_to_move = int(target_steps)

    if direction == instructions.Direction.CW:
        write_pin(pin=TBL_DIR_PIN, high=TBL_INVERT_DIRECTION)
    elif direction == instructions.Direction.CCW:
        write_pin(pin=TBL_DIR_PIN, high=not TBL_INVERT_DIRECTION)
    elif direction == instructions.Direction.IGNORED:
        return
    else:
        logger.warning(f"Direction {direction} not recognized!")
        raise InvalidDirectionException(direction)

    for _ in range(abs(steps_to_move)):
        step()
        sleep_micro_seconds(TBL_STP_COOLDOWN_MICRO_SECONDS)

    actual_rotation = (steps_to_move / STP_P_REV) * 360.0

    error_degrees = adjusted_degrees - actual_rotation
    if direction == instructions.Direction.CW:
        move_tbl_degrees.error -= error_degrees
    else:
        move_tbl_degrees.error += error_degrees

    logger.debug(f"Table Error: {move_tbl_degrees.error:.4f}")
