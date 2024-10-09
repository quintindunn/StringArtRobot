import sys
import threading

from robot.string_bot import StringBot
from robot.ui import UI

from web_interface.web import app

import logging

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
