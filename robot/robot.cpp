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
    std::vector<std::string> segments = split(instructions, " ");
    const std::string instruction = toLower(segments.at(0));

    Command* command = nullptr;

    if (instruction == "rot") {
        command = new Rotate(segments);
    } else if (instruction == "pn") {
        command = new PlaceNail(segments);
    } else if (instruction == "bp") {
        command = new Beep(segments);
    } else if (instruction == "sp") {
        command = new Sleep(segments);
    }

    if (command != nullptr)
        command->execute();
}

angle Robot::getTableAngle() {
    return this->tableAngle;
}

angle Robot::rotateTable(int degrees, int direction, int speed) {
    return 0;
}

