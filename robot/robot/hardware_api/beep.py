import logging
import time

from .config import BUZZER_PIN
from .write_pin import write_pin

logger = logging.getLogger("robot.hardware_api.beep")


def beep(duration_ms):
    write_pin(BUZZER_PIN, high=True)
    time.sleep(duration_ms/1000)
    write_pin(BUZZER_PIN, high=False)
