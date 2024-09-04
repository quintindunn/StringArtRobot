//
// Created by Quintin Dunn on 9/2/24.
//

#ifndef ROBOT_H
#define ROBOT_H
#include <cstdint>
#include <string>
#include <map>


typedef unsigned short angle;
typedef uint8_t tool_id;
typedef uint8_t speed;

#define SERVO_TOOL_IDS_PIN_MAP {(tool_id) 1}
#define STEPPER_TOOL_IDS_PIN_MAP {(tool_id) 2}

const std::map<tool_id, int> pin_map = {
        {1, 5},
        {2, 6}
};

class Robot {
private:
    tool_id tableId = 0;
    tool_id servoId = 0;
    angle tableAngle = 0;
public:
    Robot();
    ~Robot();

    static void parseInstruction(const std::string& instruction);



    angle getTableAngle();
    angle rotateTable(int degrees, int direction, int speed);
};



#endif //ROBOT_H
