from instruction_interpreter.instructions import parse_multiline_str, instruction_parser

if __name__ == '__main__':
    SAMPLE_LINES = "ROT i1 d1 a51 s255\nROT i2 d-1 a212 s125\nPN p255 r255\nBP d100 r5 o1000\nSP d1000"

    commands = parse_multiline_str(SAMPLE_LINES)

    for command in commands:
        print(command.instruction)
