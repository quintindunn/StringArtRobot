import logging
import sys

from robot.string_bot import StringBot

logger = logging.getLogger("main")

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    bot = StringBot()
    bot.file_path = "./horse.stringart"

    bot.execute_file()
