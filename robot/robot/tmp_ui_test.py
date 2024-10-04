import os

from ui import UI, CTX

if __name__ == '__main__':
    ui = UI()

    print("Controls:")
    print("1 - Next")
    print("0 - Previous")
    print("2 - Select")
    print("4 - Add pseudo program")

    command = 0
    while command != -1:
        CTX['programs'].clear()
        CTX['programs'].extend(os.listdir("../stringart_files"))
        ui.update_programs()

        ui.interpret_controls(command=command)
        print("\n"*4)

        if command == 4:
            pgm = input("Program Name: ")
            CTX["programs"].append(pgm)

        lines = ui.get_lines()

        print(*lines, sep='\n')

        command = int(input("Command: "))
