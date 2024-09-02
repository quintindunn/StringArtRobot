//
// Created by Quintin Dunn on 9/2/24.
//

#include "robot.h"
#include "utils/string_utils.h"

#include <string>
#include <vector>

robot::robot() = default;

void robot::parseInstruction(const std::string& instructions) {
    std::vector<std::string> segments = split(instructions, " ");

    const std::string& instruction = segments.at(0);
    for (const std::string& parameter : segments) {

    }
}


angle robot::getTableAngle() {
    return this->tableAngle;
}

angle robot::rotateTable(int degrees, int direction, int speed) {

}
