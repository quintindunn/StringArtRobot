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
    parser.add_argument("-tbcd", help="Cooldown time between table rotation and another operation. (ms)", type=int,
                        default=1500)
    parser.add_argument("-upload", help="URL for upload", type=str, default="http://192.168.1.29:8080")

    return parser.parse_args()


def nail_to_angle(nail_idx: int):
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


def move_to_nail_instruction(current_nail: int, target_nail: int, offset_angle: float = 0.0):
    theta, direction = calculate_relative_rotation(current_nail, target_nail)
    theta += offset_angle

    return RotateTool(tool_id=parsed_args.ttid, direction=direction, speed=parsed_args.tbsp, degrees=theta)


def servo_to_angle(deg: float, fw: bool = True):
    speed = parsed_args.afws if fw else parsed_args.abws
    return RotateTool(tool_id=parsed_args.atid, direction=Direction.IGNORED, degrees=deg, speed=speed)


def rotate_table_degrees(degrees: int, direction: int, speed: int = 127):
    return RotateTool(tool_id=parsed_args.ttid, degrees=degrees, direction=direction, speed=speed)


def circle_nail_group(current_nail: int, target_nail: int):
    # Go to the nail
    instructions = []

    spacing_offset = 360 / parsed_args.pc
    middle_offset = spacing_offset / 2

    # reset servo to forward angle for travel
    instructions.append(servo_to_angle(parsed_args.faa, fw=True))

    # seq: B
    instructions.append(move_to_nail_instruction(current_nail, target_nail))
    reference_instruction = instructions[-1]
    b_dir = reference_instruction.direction
    inv_direction = Direction.CW if b_dir == Direction.CCW else Direction.CW if b_dir == Direction.CCW else b_dir

    if parsed_args.tbcd != -1:
        instructions.append(Sleep(duration_ms=parsed_args.tbcd))

    # seq: D
    instructions.append(rotate_table_degrees(middle_offset * 4, inv_direction, speed=parsed_args.tbsp))

    if parsed_args.tbcd != -1:
        instructions.append(Sleep(duration_ms=parsed_args.tbcd))

    # seq: E
    instructions.append(servo_to_angle(parsed_args.baa, fw=False))

    # seq: F
    b_dir = reference_instruction.direction
    inv_direction = Direction.CW if b_dir == Direction.CCW else Direction.CW if b_dir == Direction.CCW else b_dir
    instructions.append(rotate_table_degrees(middle_offset * 2, inv_direction, speed=parsed_args.tbsp))

    if parsed_args.tbcd != -1:
        instructions.append(Sleep(duration_ms=parsed_args.tbcd))

    # seq: G
    instructions.append(servo_to_angle(parsed_args.faa, fw=True))

    # seq: H
    instructions.append(rotate_table_degrees(middle_offset, b_dir, speed=parsed_args.tbsp))

    if parsed_args.tbcd != -1:
        instructions.append(Sleep(duration_ms=parsed_args.tbcd))

    return instructions


def construct():
    current_nail = 0
    with open(parsed_args.i) as f:
        pins = list(map(int, f.read().split(",")))

    instruction_groups = []

    for pin in pins[1:]:
        instruction_groups.append(f"# {current_nail} -> {pin}")
        instruction_groups.extend(circle_nail_group(current_nail=current_nail, target_nail=pin))
        current_nail = pin

    return instruction_groups


def dump(instruction_groups: list[str | BaseInstruction]):
    with open(parsed_args.o, 'w') as f:
        f.write("\n".join(map(str, instruction_groups)))


if __name__ == '__main__':
    parsed_args = arg_parser()
    dump(construct())

    if parsed_args.upload:
        with open(parsed_args.o, 'rb') as f:
            request = requests.post(parsed_args.upload, files={"files": f})
            print(request, request.text)