//
// Created by Jason on 9/2/2024.
//

#include "Sleep.h"

#include <format>
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

std::string Sleep::Rebuild() {
    return std::format("SP d{}", this->duration_ms);
}