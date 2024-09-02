//
// Created by Quintin Dunn on 9/2/2024.
//

#ifndef STRINGARTROBOT_BEEP_H
#define STRINGARTROBOT_BEEP_H

#include "instructions.h"

#include <vector>
#include <string>

class Beep : public Command {
private:
    duration durations_ms;
    unsigned int repeat;
    duration off_time_ms;
public:
    explicit Beep(std::vector<std::string>);

    void execute() override;

    std::string Rebuild();
};


#endif //STRINGARTROBOT_BEEP_H
