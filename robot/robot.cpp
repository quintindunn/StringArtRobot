//
// Created by Quintin Dunn on 9/2/24.
//

#include "robot.h"
#include "instructions/instructions.h"
#include "utils/string_utils.h"

#include <string>
#include <vector>

Robot::Robot() = default;
Robot::~Robot() = default;

void Robot::parseInstruction(const std::string& instructions) {
    std::vector<std::string> segments = split(instructions, " ", 1);
    const std::string instruction = toLower(segments.at(0));

    if (instruction == "rot") {
        Rotate command = *new Rotate(segments);
    }
    /*else if (instruction == "") {

    } else if (instruction == "")*/
}


angle Robot::getTableAngle() {
    return this->tableAngle;
}

angle Robot::rotateTable(int degrees, int direction, int speed) {
    return 0;
}

