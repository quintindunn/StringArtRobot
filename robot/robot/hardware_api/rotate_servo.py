import logging

from .config import ARM_PIN

logger = logging.getLogger("robot.hardware_api.rotate_servo")

servo = ARM_PIN


def rotate_arm_to(degrees: float):
    if not hasattr(rotate_arm_to, "arm_angle"):
        setattr(rotate_arm_to, "arm_angle", degrees)
    else:
        rotate_arm_to.arm_angle = degrees

    # TODO: Implement fully.
    logger.info(f"Rotating arm to {degrees:.3f} degrees")
