//
// Created by Quintin Dunn on 9/2/2024.
//

#include "Beep.h"
#include "instructions.h"
#include "robot.h"

#include <iostream>

Beep::Beep(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("d")) {
            duration value = std::stoi(segment.substr(1));
            this->durations_ms = value;
        } else if (segment.starts_with("r")) {
            unsigned int value = std::stoi(segment.substr(1));
            this->repeat = value;
        } else if (segment.starts_with("o")) {
            duration value = std::stoi(segment.substr(1));
            this->off_time_ms = value;
        }
    }
#ifdef DEBUG_INSTRUCTIONS
    std::cout << this->Rebuild() << std::endl;
#endif
}

std::string Beep::Rebuild() const {
    return "BP d" + std::to_string(this->durations_ms) + " r" + std::to_string(this->repeat) + " o" +
    std::to_string(this->off_time_ms);
}

void Beep::execute() {
    std::cout << "Executing " << this->Rebuild() << std::endl;
}
