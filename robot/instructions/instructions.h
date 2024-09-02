//
// Created by Quintin Dunn on 9/2/2024.
//
#define DEBUG_INSTRUCTIONS

#ifndef STRINGARTROBOT_INSTRUCTIONS_H
#define STRINGARTROBOT_INSTRUCTIONS_H

typedef unsigned long duration;

class Command {
public:
    virtual void execute() = 0;
    virtual ~Command() = default;
};

#include "Rotate.h"
#include "PlaceNail.h"
#include "Beep.h"
#include "Sleep.h"

#include "../utils/string_utils.h"

#endif //STRINGARTROBOT_INSTRUCTIONS_H
