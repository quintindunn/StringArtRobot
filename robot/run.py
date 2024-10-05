import sys
import threading

from robot.robot.string_bot import StringBot
from robot.robot.ui import UI, CTX

from web_interface.web import app

import os
import logging

from pathlib import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def launch_bot_and_ui():
    bot = StringBot()
    ui = UI(bot)
    command = 0
    while command != -1:
        ui.interpret_controls(command=command)

        ui.display()

        command = int(input("Command: "))


def launch_web():
    app.run(host="0.0.0.0", port=8080, debug=False)


if __name__ == '__main__':
    threading.Thread(target=launch_bot_and_ui, daemon=True).start()
    launch_web()
