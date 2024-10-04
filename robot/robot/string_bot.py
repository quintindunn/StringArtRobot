import logging

from typing import Iterable
from .instructions import BaseInstruction, instruction_parser

logger = logging.getLogger("robot.string_bot")


class StringBot:
    def __init__(self):
        self.file_path = ""

    def instructions(self) -> Iterable["BaseInstruction"]:
        with open(self.file_path, 'r') as f:
            for line in f:
                yield instruction_parser(line)

    def execute_file(self):
        for instruction in self.instructions():
            if instruction:
                logging.info(f"Executing {instruction.instruction}")
                try:
                    instruction.execute()
                except NotImplementedError:
                    logger.warning(f"Instruction \"{instruction.instruction.split(' ', 1)[0]}\" not implemented!")