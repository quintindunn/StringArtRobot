from .hardware_api import move_tbl_degrees, rotate_arm_to, ARM_TID, TBL_TID

import logging
import time

logger = logging.getLogger("Instructions")


def parse_multiline_str(instructions: str) -> list["BaseInstruction"]:
    commands = []
    for instruction in instructions.split("\n"):
        commands.append(instruction_parser(instruction))

    return commands


def instruction_parser(instruction: str) -> "BaseInstruction":
    instruction = instruction.split("#")[0]

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

    CW = 1
    CCW = -1

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
        direction = -99
        degrees = -99
        speed = -99

        for segment in segments[1:]:
            if segment.startswith("i"):
                i += 1
                value = int(segment.split("i", 1)[1])
                tool_id = value
            elif segment.startswith("d"):
                i += 1
                value = int(segment.split("d", 1)[1])
                direction = value
            elif segment.startswith("a"):
                i += 1
                value = float(segment.split("a", 1)[1])
                degrees = value
            elif segment.startswith("s"):
                i += 1
                value = int(segment.split("s", 1)[1])
                speed = value

        if direction not in (Direction.CW, Direction.CCW, Direction.IGNORED):
            raise ValueError(f"Direction \"{direction}\" not recognized")

        if degrees > 0:
            degrees = abs(degrees)
            direction = self._invert_direction(direction)

        if speed not in range(1, 256):
            raise ValueError(f"Speed {speed} not in range (1-255)")

        self.direction = direction
        self.degrees = degrees
        self.speed = speed
        self.tool_id = tool_id

    @staticmethod
    def _invert_direction(direction):
        # Not using direction = -direction so Direction's values can be adjusted if say we only want positive ints.
        if direction == Direction.CW:
            return Direction.CCW
        return Direction.CCW

    @property
    def instruction(self) -> str:
        return f"ROT i{self.tool_id} d{self.direction} a{self.degrees} s{self.speed}"

    def execute(self):
        if self.tool_id == ARM_TID:
            rotate_arm_to(degrees=self.degrees)
        elif self.tool_id == TBL_TID:
            move_tbl_degrees(degrees=self.degrees, direction=self.direction)


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
