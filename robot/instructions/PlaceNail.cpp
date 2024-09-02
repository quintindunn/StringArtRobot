//
// Created by Quintin Dunn on 9/2/2024.
//
#include "PlaceNail.h"
#include "instructions.h"
#include "../utils/string_utils.h"

#include <format>
#include <iostream>

// PN p<ps> r<rs>
PlaceNail::PlaceNail(std::vector<std::string> segments) {
    segments.erase(segments.begin());

    for (std::string segment : segments) {
        segment = toLower(segment);
        if (segment.starts_with("p")) {
            speed value = std::stoi(segment.substr(1));
            this->placeRate = value;
        } else if (segment.starts_with("r")) {
            speed value = std::stoi(segment.substr(1));
            this->retractRate = value;
        }
    }
#ifdef DEBUG_INSTRUCTIONS
    std::cout << this->Rebuild() << std::endl;
#endif
}

std::string PlaceNail::Rebuild() {
    return std::format("PN p{} r{}", this->placeRate, this->retractRate);
}

void PlaceNail::execute() {
    std::cout << "Executing " << this->Rebuild() << std::endl;
}
