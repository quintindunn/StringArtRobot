
import random

import requests

from instructions import Direction, RotateTool, Sleep, BaseInstruction
import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file path")
    parser.add_argument("-o", help="Output file path")
    parser.add_argument("-pc", help="Number of pins.", type=int)
    parser.add_argument("-faa", help="Forward Arm Angle.", type=float, default=10.0)
    parser.add_argument("-baa", help="Backward Arm Angle.", type=float, default=-10.0)
    parser.add_argument("-atid", help="Arm Tool Id.", type=int, default=1)
    parser.add_argument("-ttid", help="Table Tool Id.", type=int, default=0)
    parser.add_argument("-abws", help="Arm Backward Speed", type=int, default=127)
    parser.add_argument("-afws", help="Arm Forward Speed", type=int, default=127)
    parser.add_argument("-tbsp", help="Table rotation speed", type=int, default=127)
    parser.add_argument("-tbcd", help="Time between table rotation and next instruction. (ms)", type=int, default=500)
    parser.add_argument("-uploadurl", help="Url to upload the file to", type=str, default="")

    return parser.parse_args()


def nail_to_angle(nail_idx: int | float):
    nail_count = parsed_args.pc
    nail_spacing_deg = 360 / nail_count
    angle = nail_spacing_deg * nail_idx
    return angle


def calculate_relative_rotation(nail_index_1: int, nail_index_2: int) -> tuple[float, int | None]:
    angle_1 = nail_to_angle(nail_index_1) % 360
    angle_2 = nail_to_angle(nail_index_2) % 360

    theta = ((angle_2 - angle_1) + 180) % 360 - 180
    direction = Direction.CCW if theta > 0 else Direction.CW if theta < 0 else None
    theta = abs(theta)

    return theta, direction


def move_to_nail_instruction(target_nail: int):
    angle = nail_to_angle(target_nail)
    return RotateTool(tool_id=parsed_args.ttid, speed=parsed_args.tbsp, degrees=angle, absolute=True)


def servo_to_angle(deg: float, fw: bool = True):
    speed = parsed_args.afws if fw else parsed_args.abws
    return RotateTool(tool_id=parsed_args.atid, degrees=deg, speed=speed, absolute=True)


def rotate_table_to(degrees: int, speed: int = 127):
    return RotateTool(tool_id=parsed_args.ttid, degrees=degrees, speed=speed, absolute=True)


def if_tbcd_sleep(instructions: list[BaseInstruction]):
    if parsed_args.tbcd != -1:
        instructions.append(Sleep(duration_ms=parsed_args.tbcd))


def circle_nail_group(target_nail: int):
    # Go to the nail
    instructions = []

    a1 = nail_to_angle(target_nail-0.5)
    a2 = nail_to_angle(target_nail+0.5)
    home = move_to_nail_instruction(target_nail)
    fw = parsed_args.faa
    bw = parsed_args.baa

    # 1.) Rotate to the pin
    instructions.append(home)
    if_tbcd_sleep(instructions)

    # 2.) Rotate `d1` spacing/2deg
    instructions.append(rotate_table_to(a1))
    if_tbcd_sleep(instructions)

    # 3.) Arm from `fw`deg -> `bw`deg
    instructions.append(servo_to_angle(bw, fw=False))

    # 4.) Rotate `d2` `spacing`deg
    instructions.append(rotate_table_to(a2))
    if_tbcd_sleep(instructions)

    # 5.) Arm from `bw`deg -> `fw`deg
    instructions.append(servo_to_angle(fw, fw=True))

    # 6.) Rotate `d1` `spacing`deg
    instructions.append(rotate_table_to(a1))
    if_tbcd_sleep(instructions)

    # 7.) Arm from `fw`deg -> `bw`deg
    instructions.append(servo_to_angle(bw, fw=False))

    # 8.) Rotate `d2` `spacing`deg
    instructions.append(rotate_table_to(a2))

    # 9.) Arm from `bw`deg to `fw`deg
    instructions.append(servo_to_angle(fw, fw=True))

    # 10.) Reset to initial angle.
    instructions.append(home)
    if_tbcd_sleep(instructions)

    return instructions


def pre_processing() -> list[BaseInstruction | str]:
    queue = [
        servo_to_angle(parsed_args.faa, fw=True)
    ]

    return queue


def construct():
    current_nail = 0
    with open(parsed_args.i) as f:
        pins = list(map(int, f.read().split(",")))

    instruction_groups = pre_processing()

    for pin in pins[1:]:
        instruction_groups.append(f"# {current_nail} -> {pin}")
        instruction_groups.extend(circle_nail_group(target_nail=pin))
        current_nail = pin

    return instruction_groups


def dump(instruction_groups: list[str | BaseInstruction]):
    with open(parsed_args.o, 'w') as f:
        f.write("\n".join(map(str, instruction_groups)))


if __name__ == '__main__':
    parsed_args = arg_parser()
    dump(construct())
    if parsed_args.uploadurl:
        with open(parsed_args.o, 'rb') as f:
            request = requests.post(parsed_args.uploadurl, files={"files": f})
