//
// Created by Quintin Dunn on 9/2/2024.
//

#include "Sleep.h"

#include <iostream>


Sleep::Sleep(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("d")) {
            duration value = std::stoi(segment.substr(1));
            this->duration_ms = value;
        }
    }
#ifdef DEBUG_INSTRUCTIONS
    std::cout << this->Rebuild() << std::endl;
#endif
}

std::string Sleep::Rebuild() const {
    return "SP d" + std::to_string(this->duration_ms);
}

void Sleep::execute() {
    std::cout << "Executing " << this->Rebuild() << std::endl;
}
