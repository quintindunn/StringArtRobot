from typing import Union

from .hardware_api import move_tbl_degrees, rotate_arm_to, beep, ARM_TID, TBL_TID

import logging
import time

logger = logging.getLogger("Instructions")


def parse_multiline_str(instructions: str) -> list["BaseInstruction"]:
    commands = []
    for instruction in instructions.split("\n"):
        commands.append(instruction_parser(instruction))

    return commands


def instruction_parser(instruction: str) -> Union["BaseInstruction", None]:
    instruction = instruction.split("#")[0].lstrip(" ")
    if not instruction:
        return None

    segments = instruction.split(" ")
    instruction_type = segments[0].lower()

    command = None

    if instruction_type == "rot":
        logger.debug("Parsing RotateTool instruction.")
        command = RotateTool(segments)
    elif instruction_type == "pn":
        logger.debug("Parsing PlaceNail instruction.")
        command = PlaceNail(segments)
    elif instruction_type == "bp":
        logger.debug("Parsing Beep instruction.")
        command = Beep(segments)
    elif instruction_type == "sp":
        logger.debug("Parsing Sleep instruction.")
        command = Sleep(segments)
    else:
        logger.warning(f"Instruction \"{instruction_type}\" not recognized")

    return command


class Direction:
    IGNORED = 0

    CW = -1
    CCW = 1

    UP = 1
    DOWN = -1


class BaseInstruction:
    def __init__(self):
        pass

    def execute(self):
        raise NotImplementedError("Instruction not implemented!")

    @property
    def instruction(self):
        return "#NOTIMPLEMENTED!"


class RotateTool(BaseInstruction):
    def __init__(self, segments: list[str]):
        super().__init__()

        i = 0

        tool_id = -99
        absolute = False
        degrees = -99
        speed = -99

        for segment in segments[1:]:
            if segment.startswith("i"):
                i += 1
                value = int(segment.split("i", 1)[1])
                tool_id = value
            elif segment.startswith("abs"):
                i += 1
                value = segment.split("abs", 1)[1][0] == "1"
                absolute = value
            elif segment.startswith("a"):
                i += 1
                value = float(segment.split("a", 1)[1])
                degrees = value
            elif segment.startswith("s"):
                i += 1
                value = int(segment.split("s", 1)[1])
                speed = value

        if speed not in range(1, 256):
            raise ValueError(f"Speed {speed} not in range (1-255)")

        self.degrees = degrees
        self.speed = speed
        self.tool_id = tool_id
        self.absolute = absolute

    @property
    def instruction(self) -> str:
        return f"ROT i{self.tool_id} a{self.degrees} s{self.speed} abs{int(self.absolute)}"

    def execute(self):
        if self.tool_id == ARM_TID:
            rotate_arm_to(self.degrees)
        elif self.tool_id == TBL_TID:
            move_tbl_degrees(self.degrees)


class PlaceNail(BaseInstruction):
    def __init__(self, segments: list[str]):
        super().__init__()

        place_rate = None
        retract_rate = None

        for segment in segments[1:]:
            segment = segment.lower()
            if segment.startswith("p"):
                value = int(segment.split("p", 1)[1])
                place_rate = value
            elif segment.startswith("r"):
                value = int(segment.split("r", 1)[1])
                retract_rate = value

        if place_rate not in range(1, 256):
            raise ValueError(f"place_rate {place_rate} not in range 1-255 (inclusive)")
        if retract_rate not in range(1, 256):
            raise ValueError(f"retract_rate {retract_rate} not in range 1-255 (inclusive)")

        self.place_speed = place_rate
        self.retraction_speed = retract_rate

    @property
    def instruction(self) -> str:
        return f"PN p{self.place_speed} r{self.retraction_speed}"

    def execute(self):
        raise NotImplementedError("Placing Nails has not been implemented!")


class Beep(BaseInstruction):
    def __init__(self, segments: list[str]):
        super().__init__()

        self.durations_ms = None
        self.repeat = None
        self.off_time_ms = None

        for segment in segments[1:]:
            segment = segment.lower()
            if segment.startswith("d"):
                value = int(segment.split("d", 1)[1])
                self.durations_ms = value
            elif segment.startswith("r"):
                value = int(segment.split("r", 1)[1])
                self.repeat = value
            elif segment.startswith("o"):
                value = int(segment.split("o", 1)[1])
                self.off_time_ms = value

        if self.durations_ms is not None and self.durations_ms < 0:
            raise ValueError("Duration cannot be less than 0.")
        if self.off_time_ms is not None and self.off_time_ms < 0:
            raise ValueError("Off time cannot be less than 0.")
        if isinstance(self.repeat, int) and self.repeat < 0:
            raise ValueError("Repeat cannot be less than 0.")
        if self.repeat is None:
            self.repeat = 1

    @property
    def instruction(self):
        return f"BP d{self.durations_ms} r{self.repeat} o{self.off_time_ms}"

    def execute(self):
        count = 0
        while count > self.repeat:
            beep(self.durations_ms)

            count += 1
            if count > self.repeat:
                time.sleep(self.off_time_ms/1000)


class Sleep(BaseInstruction):
    def __init__(self, segments: list[str]):
        super().__init__()

        self.duration_ms = None

        for segment in segments[1:]:
            segment = segment.lower()
            if segment.startswith("d"):
                value = int(segment.split("d", 1)[1])
                self.duration_ms = value

        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("Duration cannot be less than 0.")

    @property
    def instruction(self):
        return f"SP d{self.duration_ms}"

    def execute(self):
        time.sleep(self.duration_ms/1000)
