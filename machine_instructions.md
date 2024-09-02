# DOCUMENTATION:
## Rotate Table:
### Parameters:
    * degrees - How many degrees to rotate
    * direction - Which direction to rotate (Direction.CW | Direction.CCW)
    * speed - 0-255 How quickly to rotate the table
### Instruction:
    * ROT d<direction> a<degrees> s<speed>
ROT d<direction> a<degrees> s<speed>
MT i<tool_id> x<delta_x> y<delta_y> s<speed>

## Place Nail:
### Parameters:
    * ps - 0-255 How quickly to place the nail
    * rs - 0-255 How quickly to retract the tool
### Instruction:
    * PN p<ps> r<rs>

## Move Tool:
### Parameters:
    * tool_id - The numerical ID of the tool
    * delta_x - The change in the `x` value
    * delta_y - The change in the `y` value
    * speed - 0-255 How quickly to move the tool
### Instruction:
    * MT i<tool_id> x<delta_x> y<delta_y> s<speed>

## Beep:
### Parameters:
    * duration_ms - how long to beep for (ms)
    * repeat - How many times should it repeat for
    * off_time_ms - How long between beeps (ms)
### Instruction:
    * BP d<duration_ms> r<repeat> o<off_time_ms>

## Sleep:
### Parameters:
    * duration_ms - How long to sleep for (ms)
### Instruction:
    * SP d<duration_ms>