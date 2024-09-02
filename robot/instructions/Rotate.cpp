//
// Created by Quintin Dunn on 9/2/2024.
//

#include "Rotate.h"
#include "../utils/string_utils.h"

#include <vector>
#include <string>
#include <format>


// ROT d<direction> a<degrees> s<speed>
Rotate::Rotate(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("d")) {
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
}

std::string Rotate::Rebuild() {
    return std::format("ROT d% a% s%", this->direction, this->degrees, this->rate);
}