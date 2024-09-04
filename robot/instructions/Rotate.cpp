//
// Created by Quintin Dunn on 9/2/2024.
//

#include "instructions.h"
#include "Rotate.h"

#include <vector>
#include <string>
#include <iostream>

#include "robot.h"
#include "../controls/controls.h"

#define CHECK_COUNT 4

// ROT d<direction> a<degrees> s<speed>
Rotate::Rotate(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    bool checks[CHECK_COUNT];
    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("i")) {
            checks[0] = true;
            tool_id value = std::stoi(segment.substr(1));
            this->id = value;
        } else if (segment.starts_with("d")) {
            checks[1] = true;
            int value = std::stoi(segment.substr(1));
            this->direction = value;
        } else if (segment.starts_with("a")) {
            checks[2] = true;
            angle value = std::stoi(segment.substr(1));
            this->degrees = value;
        } else if (segment.starts_with("s")) {
            checks[3] = true;
            speed value = std::stoi(segment.substr(1));
            this->rate = value;
        }
    }
    int i = 0;
    for (bool check : checks) {
        if (check)
            i++;
    }

    if (i != CHECK_COUNT) {
        std::cerr << "Invalid instruction!" << std::endl;
    }

#ifdef DEBUG_INSTRUCTIONS
    std::cout << this->Rebuild() << std::endl;
#endif
}

std::string Rotate::Rebuild() const {
    return "ROT i" + std::to_string(this->id) + " d" + std::to_string(this->direction) +
    " a" + std::to_string(this->degrees) + " s" + std::to_string(this->rate);
}

void Rotate::execute() {
    bool stepper = false;

    for (tool_id stepper_id : STEPPER_TOOL_IDS_PIN_MAP) {
        if (this->id == stepper_id) {
            stepper = true;
            break;
        }
    }
    int pin = pin_map.at(this->id);

    if (stepper) {
        stepperStepDegrees(pin, this->direction, this->degrees, this->rate);
    } else {
        servoToAngle(pin, this->degrees, this->rate);
    }
    std::cout << "Executing " << this->Rebuild() << std::endl;
}
