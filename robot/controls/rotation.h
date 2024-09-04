//
// Created by Quintin Dunn on 9/4/2024.
//

#ifndef STRINGARTROBOT_ROTATION_H
#define STRINGARTROBOT_ROTATION_H

#include "../instructions/instructions.h"

void stepperStepDegrees(int pin, int direction, angle degrees, speed rate);
void servoToAngle(int pin, angle degrees, speed rate);

#endif //STRINGARTROBOT_ROTATION_H
