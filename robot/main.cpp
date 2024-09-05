//
// Created by Quintin Dunn on 9/2/24.
//

#include "robot.h"
#include <iostream>

int main() {
    std::string SAMPLE_LINES = "ROT i1 d1 a51 s255\nROT i2 d-1 a212 s125\nPN p255 r255\nBP d100 r5 o1000\nSP d1000";
    Robot robot = *new Robot();

    std::cout << "Individual instructions: " << std::endl;
    Robot::parseInstruction("ROT i1 d1 a51 s255");
    Robot::parseInstruction("ROT i2 d-1 a212 s125");
    Robot::parseInstruction("PN p255 r255");
    Robot::parseInstruction("BP d100 r5 o1000");
    Robot::parseInstruction("SP d1000");

    std::cout << "\n\nMultiline instructions: " << std::endl;
    robot.ParseMultilineString(SAMPLE_LINES);
    return 0;
}