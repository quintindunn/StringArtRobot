import logging
import time

from .config import ARM_PIN, ARM_TIME_PER_60_DEG, ARM_TIME_PER_60_DEG_SAFETY, DEV_NO_GPIO

if not DEV_NO_GPIO:
    from gpiozero import Servo
    from gpiozero.pins.pigpio import PiGPIOFactory

    factory = PiGPIOFactory()

    servo = Servo(ARM_PIN, pin_factory=factory, min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000)


logger = logging.getLogger("robot.hardware_api.rotate_servo")

TIME_PER_DEG = (ARM_TIME_PER_60_DEG + ARM_TIME_PER_60_DEG_SAFETY) / 60


def rotate_arm_to(degrees: float):
    degrees = max(-90.0, min(90.0, degrees)) / 90

    if not hasattr(rotate_arm_to, "arm_angle"):
        setattr(rotate_arm_to, "arm_angle", degrees)
        old = 0.0
    else:
        old = rotate_arm_to.arm_angle
        rotate_arm_to.arm_angle = degrees

    # TODO: Implement servo rotation.
    logger.info(f"Rotating arm to {degrees*90:.3f} degrees")

    # If we're developing without GPIO.
    if not DEV_NO_GPIO:
        servo.value = degrees

    deg_difference = abs(old-degrees)
    time.sleep(deg_difference * TIME_PER_DEG)
