//
// Created by Quintin Dunn on 9/4/2024.
//

#include "controls.h"
#include <iostream>

void servoToAngle(int pin, angle degrees, speed rate) {
    std::cout << "Turning servo on pin " << pin << " to " << degrees << "degrees at rate " << rate << "." << std::endl;
}

void stepperToAngle(int pin, int direction, angle degrees, speed rate) {
    std::cout << "Turning stepper on pin " << pin << " " << degrees << "degrees " << "in direction " << direction <<
    "at rate " << rate << "." << std::endl;
}