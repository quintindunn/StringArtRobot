//
// Created by Quintin Dunn on 9/2/24.
//
#include "robot.h"

int main() {
    Robot robot = *new Robot();
    robot.parseInstruction("ROT d1 a51 s255");
    robot.parseInstruction("PN p255 r255");
    return 0;
}