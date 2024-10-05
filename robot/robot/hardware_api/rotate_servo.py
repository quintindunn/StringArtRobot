import logging
import time

from .config import ARM_PIN, ARM_TIME_PER_60_DEG, ARM_TIME_PER_60_DEG_SAFETY

logger = logging.getLogger("robot.hardware_api.rotate_servo")

servo = ARM_PIN
TIME_PER_DEG = (ARM_TIME_PER_60_DEG + ARM_TIME_PER_60_DEG_SAFETY) / 60


def rotate_arm_to(degrees: float):
    if not hasattr(rotate_arm_to, "arm_angle"):
        setattr(rotate_arm_to, "arm_angle", degrees)
        old = 0.0
    else:
        old = rotate_arm_to.arm_angle
        rotate_arm_to.arm_angle = degrees

    # TODO: Implement fully.
    logger.info(f"Rotating arm to {degrees:.3f} degrees")

    deg_difference = abs(old-degrees)
    time.sleep(deg_difference * TIME_PER_DEG)
