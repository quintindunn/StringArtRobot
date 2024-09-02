//
// Created by Quintin Dunn on 9/2/2024.
//

#include "instructions.h"
#include "Rotate.h"

#include <vector>
#include <string>
#include <format>
#include <iostream>


// ROT d<direction> a<degrees> s<speed>
Rotate::Rotate(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("i")) {
            tool_id value = std::stoi(segment.substr(1));
            this->id = value;
        } else if (segment.starts_with("d")) {
            int value = std::stoi(segment.substr(1));
            this->direction = value;
        } else if (segment.starts_with("a")) {
            angle value = std::stoi(segment.substr(1));
            this->degrees = value;
        } else if (segment.starts_with("s")) {
            speed value = std::stoi(segment.substr(1));
            this->rate = value;
        }
    }
#ifdef DEBUG_INSTRUCTIONS
    std::cout << this->Rebuild() << std::endl;
#endif
}

std::string Rotate::Rebuild() {
    return std::format("ROT i{} d{} a{} s{}", this->id, this->direction, this->degrees, this->rate);
}

void Rotate::execute() {
    std::cout << "Executing " << this->Rebuild() << std::endl;
}
