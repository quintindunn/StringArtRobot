"""
# DOCUMENTATION:
## Rotate Tool:
    ### Parameters:
        * tool_id - The id of the tool to rotate
        * degrees - How many degrees to rotate
        * direction - Which direction to rotate (Direction.CW | Direction.CCW)
        * speed - 0-255 How quickly to rotate the table
    ### Instruction:
        * ROT i<tool_id> d<direction> a<degrees> s<speed>

## Place Nail:
    ### Parameters:
        * ps - 0-255 How quickly to place the nail
        * rs - 0-255 How quickly to retract the tool
    ### Instruction:
        * PN p<ps> r<rs>

## Beep:
    ### Parameters:
        * duration_ms - how long to beep for (ms)
        * repeat - How many times should it repeat for
        * off_time_ms - How long between beeps (ms)
    ### Instruction:
        * BP d<duration_ms> r<repeat> o<off_time_ms>

## Sleep:
    ### Parameters:
        * duration_ms - How long to sleep for (ms)
    ### Instruction:
        * SP d<duration_ms>
"""


class Direction:
    CW = 1
    CCW = -1

    IGNORED = 0

    UP = 1
    DOWN = -1


class BaseInstruction:
    @property
    def instruction(self):
        return ""

    def __repr__(self):
        return self.instruction


class RotateTool(BaseInstruction):
    def __init__(self, tool_id: int, degrees: float, direction: int, speed: int):
        if direction not in (Direction.CW, Direction.CCW, Direction.IGNORED):
            raise ValueError(f"Direction \"{direction}\" not recognized")

        if degrees > 0:
            degrees = abs(degrees)
            direction = self._invert_direction(direction)

        if speed not in range(1, 255):
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

        if direction == Direction.IGNORED:
            return Direction.IGNORED

        return Direction.CCW

    @property
    def instruction(self) -> str:
        return f"ROT i{self.tool_id} d{self.direction} a{self.degrees} s{self.speed}"


class PlaceNail(BaseInstruction):
    def __init__(self, place_speed: int, retraction_speed: int):
        if place_speed not in range(1, 256):
            raise ValueError(f"place_speed {place_speed} not in range 1-255 (inclusive)")
        if retraction_speed not in range(1, 256):
            raise ValueError(f"retraction_speed {retraction_speed} not in range 1-255 (inclusive)")

        self.place_speed = place_speed
        self.retraction_speed = retraction_speed

    @property
    def instruction(self) -> str:
        return f"PN p{self.place_speed} r{self.retraction_speed}"

    def __str__(self):
        return self.instruction


class Beep(BaseInstruction):
    def __init__(self, duration_ms: int, repeat: int | None = None, off_time_ms: int = 100):
        if duration_ms < 0:
            raise ValueError("Duration cannot be less than 0.")
        if off_time_ms < 0:
            raise ValueError("Off time cannot be less than 0.")

        if isinstance(repeat, int) and repeat < 0:
            raise ValueError("Repeat cannot be less than 0.")

        if repeat is None:
            repeat = 1

        self.duration = duration_ms
        self.off_time = off_time_ms
        self.repeat = repeat

    @property
    def instruction(self):
        return f"BP d{self.duration} r{self.repeat} o{self.off_time}"

    def __str__(self):
        return self.instruction


class Sleep(BaseInstruction):
    def __init__(self, duration_ms: int):
        if duration_ms < 0:
            raise ValueError("Duration cannot be less than 0.")

        self.duration = duration_ms

    @property
    def instruction(self):
        return f"SP d{self.duration}"

    def __str__(self):
        return self.instruction
