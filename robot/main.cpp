//
// Created by Quintin Dunn on 9/2/24.
//

#include "robot.h"

int main() {
    Robot robot = *new Robot();
    Robot::parseInstruction("ROT i1 d1 a51 s255");
    Robot::parseInstruction("PN p255 r255");
    Robot::parseInstruction("BP d100 r5 o1000");
    Robot::parseInstruction("SP d1000");
    return 0;
}