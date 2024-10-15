from typing import Any
from .string_bot import StringBot
from .hardware_api import move_tbl_degrees, rotate_arm_to, display_line, display_final, clear

from pathlib import Path

import os
import threading

VERSION = "0.1.0"

ROW_COUNT = 4
BASE_Y_OFFSET = 1

TABLE_STEP_SIZE = 0.2    # deg
ARM_STEP_SIZE = 1        # deg

DEFAULT_BEHAVIOR = -1    # worlds easiest implemented
DO_NOTHING = -2          # worlds easiest implemented
PROGRAM_FLOW_CODE = 0    # implemented
TABLE_CW_FLOW_CODE = 1   # NOT
TABLE_CCW_FLOW_CODE = 2  # NOT
ARM_CW_FLOW_CODE = 3     # NOT
ARM_CCW_FLOW_CODE = 4    # NOT
PAUSE_FLOW_CODE = 5      # implemented
CANCEL_FLOW_CODE = 6     # implemented

PAUSE_LINE_IDX = 1
TABLE_ANGLE_LINE_IDX = 5
ARM_ANGLE_LINE_IDX = 6

BASE_FILE_PATH = Path("./stringart_files/")

CTX = {
    "completed": 0.0,
    "arm_angle": 0,
    "table_angle": 0,
    "current_program": None,

    "programs": []
}


class Page:
    def __init__(self, lines: list[list[str | Any]], data_indices: list[[int, int]]):
        self.lines = lines
        self.data_indices = data_indices

        self.line_idx = BASE_Y_OFFSET
        self.y_offset = 0

    def __str__(self):
        return self.lines[0][0]


class UI:
    def __init__(self, robot: StringBot):
        self.bot = robot

        self.home_page: Page = Page(lines=[], data_indices=[])
        self.status_page: Page = Page(lines=[], data_indices=[])
        self.controls_page: Page = Page(lines=[], data_indices=[])
        self.table_controls_page: Page = Page(lines=[], data_indices=[])
        self.arm_controls_page: Page = Page(lines=[], data_indices=[])
        self.programs_page: Page = Page(lines=[], data_indices=[])

        self.current_page: Page = self.home_page

        self.init()

    def flow_interpreter(self, code: int):
        if code == PROGRAM_FLOW_CODE:
            filename = self.current_page.lines[self.current_page.line_idx][0]
            self.bot.file_path = BASE_FILE_PATH / filename
            CTX['current_program'] = filename

            thread = threading.Thread(target=self.bot.execute_file, daemon=True)
            thread.start()
        elif code == PAUSE_FLOW_CODE:
            self.bot.pause = not self.bot.pause

        elif code == CANCEL_FLOW_CODE:
            self.bot.cancel = True

        elif code in (ARM_CW_FLOW_CODE, ARM_CCW_FLOW_CODE):
            direction = -1 if code == ARM_CW_FLOW_CODE else 1
            current_angle = CTX['arm_angle']
            new_angle = current_angle + (direction * ARM_STEP_SIZE)
            rotate_arm_to(new_angle)

    def init_home_page(self):
        lines = [
            [f"StringBot V{VERSION}", self.current_page],
            [f"Status", self.status_page],
            [f"Controls", self.controls_page],
            [f"Programs", self.programs_page],
            [f".", self.home_page],
        ]
        data_indices = [[0, DO_NOTHING]]

        self.home_page.lines.extend(lines)
        self.home_page.data_indices.extend(data_indices)

    def init_status_page(self):
        lines = [
            [f"Status", self.status_page],
            [f"Program: {CTX['current_program']}", self.status_page],
            [f"Complete: {CTX['completed'] * 100:.2f}", self.status_page],
            [f"..", self.home_page]
        ]

        data_indices = [[0, DO_NOTHING]]

        self.status_page.lines.extend(lines)
        self.status_page.data_indices.extend(data_indices)

    def update_status(self):
        CTX['completed'] = self.bot.line_number / self.bot.line_count if self.bot.line_count else 0.0

        program_line = f"Program: {CTX['current_program']}"
        percent_line = f"Complete: {CTX['completed'] * 100:.2f}"

        self.status_page.lines[1][0] = program_line
        self.status_page.lines[2][0] = percent_line

    def init_controls_page(self):
        lines = [
            ["Controls", self.controls_page],       # DO NOTHING
            ["Pause", self.controls_page],          # PAUSE
            ["Cancel", self.controls_page],         # CANCEL
            ["Table", self.table_controls_page],
            ["Arm", self.arm_controls_page],
            ["Table Angle: ", self.controls_page],  # DO NOTHING
            ["Arm Angle: ", self.controls_page],    # DO NOTHING
            ["..", self.home_page]
        ]

        data_indices = [
            [0, DO_NOTHING],
            [1, PAUSE_FLOW_CODE],
            [2, CANCEL_FLOW_CODE],
            [5, DO_NOTHING],
            [6, DO_NOTHING]
        ]

        self.controls_page.lines.extend(lines)
        self.controls_page.data_indices.extend(data_indices)

    def update_controls(self):
        if hasattr(rotate_arm_to, "arm_angle"):
            CTX['arm_angle'] = rotate_arm_to.arm_angle
        if hasattr(move_tbl_degrees, "current_angle"):
            CTX['table_angle'] = move_tbl_degrees.current_angle

        table_angle = f"Table Angle: {CTX['table_angle']:.2f} DEG"
        arm_angle = f"Arm Angle: {CTX['arm_angle']:.2f} DEG"

        self.controls_page.lines[PAUSE_LINE_IDX][0] = "Pause" if not self.bot.pause else "Unpause"

        self.controls_page.lines[TABLE_ANGLE_LINE_IDX][0] = table_angle
        self.controls_page.lines[ARM_ANGLE_LINE_IDX][0] = arm_angle

    def init_table_controls_page(self):
        lines = [
            ["Controls - Table", self.table_controls_page],
            ["Table - CW", self.table_controls_page],
            ["Table - CCW", self.table_controls_page],
            ["..", self.controls_page]
        ]

        data_indices = [
            [0, DO_NOTHING],
            [1, TABLE_CW_FLOW_CODE],
            [2, TABLE_CCW_FLOW_CODE]
        ]

        self.table_controls_page.lines.extend(lines)
        self.table_controls_page.data_indices.extend(data_indices)

    def init_arm_controls_page(self):
        lines = [
            ["Controls - Arm", self.arm_controls_page],
            ["Arm - CW", self.arm_controls_page],
            ["Arm - CCW", self.arm_controls_page],
            ["..", self.controls_page]
        ]

        data_indices = [
            [0, DO_NOTHING],
            [1, ARM_CW_FLOW_CODE],
            [2, ARM_CCW_FLOW_CODE]
        ]

        self.arm_controls_page.lines.extend(lines)
        self.arm_controls_page.data_indices.extend(data_indices)

    def init_programs_page(self):
        lines = [
            ["Programs", self.programs_page],
            ["..", self.home_page]
        ]

        data_indices = [
            [0, DO_NOTHING]
        ]

        self.programs_page.lines.extend(lines)
        self.programs_page.data_indices.extend(data_indices)

    def update_programs(self):
        init_size = len(CTX["programs"])
        CTX['programs'].clear()
        CTX['programs'].extend(os.listdir(Path("./stringart_files").absolute()))
        if init_size != len(CTX["programs"]):
            self.programs_page.line_idx = BASE_Y_OFFSET

        self.programs_page.lines.clear()
        self.programs_page.data_indices.clear()

        lines = [["Programs", self.programs_page]]
        data_indices = [[0, DO_NOTHING]]

        for program in CTX["programs"]:
            lines.append([program, self.programs_page])
            data_idx = len(lines) - 1
            data_indices.append([data_idx, PROGRAM_FLOW_CODE])

        lines.append(["..", self.home_page])
        self.programs_page.lines.extend(lines)
        self.programs_page.data_indices.extend(data_indices)

    def init(self):
        self.init_home_page()
        self.init_status_page()
        self.init_controls_page()
        self.init_table_controls_page()
        self.init_arm_controls_page()
        self.init_programs_page()

    def get_lines(self):
        self.update_status()
        self.update_programs()
        self.update_controls()

        buffer = []
        # Ideal conditions, just list from idx-1 -> idx+ROW_COUNT
        for i in range(max(self.current_page.line_idx - 1, 0), len(self.current_page.lines)):
            if i - self.current_page.line_idx >= ROW_COUNT - 1:
                break
            selection = self.current_page.line_idx
            line = f"* {self.current_page.lines[i][0]}" if i == selection else f"| {self.current_page.lines[i][0]}"
            line = line[:20]  # Get the first 20 characters
            buffer.append(line)

        # Calculate the missing item count
        fillers = ROW_COUNT - len(buffer)
        if len(self.current_page.lines) < fillers + len(buffer):
            fillers = len(self.current_page.lines) - len(buffer)

        # Try to put the items at the start of the buffer (start idx is too far down to do ideal method)
        start_idx = self.current_page.line_idx - 1 - fillers
        if start_idx >= 0:
            for i in range(start_idx + fillers - 1, start_idx - 1, -1):
                line = f"| {self.current_page.lines[i][0]}"
                line = line[:20]  # Get the first 20 characters
                buffer.insert(0, line)
        elif start_idx == -2:
            # Put filler items at the end of the buffer (start idx is too far up for ideal method)
            idx = len(buffer) - 1 + fillers
            line = f"| {self.current_page.lines[idx][0]}"
            line = line[:20]  # Get the first 20 characters
            buffer.append(line)

        return buffer

    def display(self):
        lines = self.get_lines()
        clear()
        for k, v in enumerate(lines):
            display_line(k, v)
        display_final()

    def interpret_controls(self, command):
        if command == 0:
            idx = self.current_page.line_idx - 1
            if idx < 0:
                idx = 0
            self.current_page.line_idx = idx

        elif command == 1:
            idx = self.current_page.line_idx + 1
            if idx > len(self.current_page.lines) - 1:
                idx = len(self.current_page.lines) - 1
            self.current_page.line_idx = idx

        elif command == 2:
            current_idx = self.current_page.line_idx
            code = -1

            for idx, pair_code in self.current_page.data_indices:
                if current_idx == idx:
                    code = pair_code
                    break

            if code != -1:
                print(f"DATALINE {self.current_page.lines[current_idx][0]}, CODE: {code}")
                self.flow_interpreter(code)
            else:
                self.current_page = self.current_page.lines[current_idx][1]
                self.current_page.line_idx = 1
