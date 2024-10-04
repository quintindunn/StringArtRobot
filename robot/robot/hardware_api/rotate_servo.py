import logging

from .config import ARM_PIN

logger = logging.getLogger("robot.hardware_api.rotate_servo")

servo = ARM_PIN


def rotate_arm_to(degrees: float):
    # TODO: Implement fully.
    logger.info(f"Rotating arm to {degrees:.3f} degrees")
