import logging
import time

from typing import Iterable
from .instructions import BaseInstruction, instruction_parser

logger = logging.getLogger("robot.string_bot")


class StringBot:
    def __init__(self):
        self.executing = False
        self.file_path = ""
        self.line_number = 0.0
        self.line_count = 0
        self.cancel = False
        self.pause = False

    def get_file_metadata(self):
        i = 0
        with open(self.file_path, 'r') as f:
            for line in f:
                if not line.lstrip(" ").startswith("#"):
                    i += 1
        self.line_count = i

    def instructions(self) -> Iterable["BaseInstruction"]:
        self.get_file_metadata()
        with open(self.file_path, 'r') as f:
            for line in f:
                yield instruction_parser(line)

    def cancel_proc(self):
        self.line_count = 0
        self.line_number = 0
        self.file_path = ""
        self.cancel = False
        self.pause = False

    def execute_file(self):
        self.executing = True
        for instruction in self.instructions():
            if self.cancel:
                self.cancel_proc()
                break
            while self.pause:
                time.sleep(0.1)

            if instruction:
                logging.info(f"Executing {instruction.instruction}")
                self.line_number += 1
                try:
                    instruction.execute()
                except NotImplementedError:
                    logger.warning(f"Instruction \"{instruction.instruction.split(' ', 1)[0]}\" not implemented!")
        self.executing = False
