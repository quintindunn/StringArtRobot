//
// Created by Quintin Dunn on 9/2/2024.
//

#ifndef STRINGARTROBOT_SLEEP_H
#define STRINGARTROBOT_SLEEP_H

#include "instructions.h"

#include <string>
#include <vector>
#include <iostream>

class Sleep : public Command {
private:
    duration duration_ms;
public:
    explicit Sleep(std::vector<std::string>);

    void execute() override;

    std::string Rebuild();
};


#endif //STRINGARTROBOT_SLEEP_H
