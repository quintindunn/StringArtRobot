//
// Created by Jason on 9/2/2024.
//

#ifndef STRINGARTROBOT_SLEEP_H
#define STRINGARTROBOT_SLEEP_H

#include "instructions.h"

#include <string>
#include <vector>

class Sleep {
private:
    duration duration_ms;
public:
    Sleep(std::vector<std::string>);

    std::string Rebuild();
};


#endif //STRINGARTROBOT_SLEEP_H
