import logging

logger = logging.getLogger("robot.hardware_api.write_pin")


def write_pin(pin: int, high: bool):
    logger.debug(f"Writing {'HIGH' if high else 'LOW'} to pin {pin}")
