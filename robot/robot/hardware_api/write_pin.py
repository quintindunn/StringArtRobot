from .config import DEV_NO_GPIO

# If we're developing without GPIO.
if not DEV_NO_GPIO:
    from gpiozero import LED
else:
    LED = (lambda x: ...)

import logging

logger = logging.getLogger("robot.hardware_api.write_pin")

pins = {}


def write_pin(pin: int, high: bool):
    if pin not in pins:
        pins[pin] = LED(pin)

    if DEV_NO_GPIO:
        logger.debug(f"Setting GPIO pin {pin} to {'high' if high else 'low'}")
        return

    if high and not DEV_NO_GPIO:
        pins[pin].on()
    else:
        pins[pin].off()

