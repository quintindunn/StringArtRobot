//
// Created by Jason on 9/2/2024.
//

#ifndef STRINGARTROBOT_PLACENAIL_H
#define STRINGARTROBOT_PLACENAIL_H

#include "robot.h"

#include <string>
#include <vector>

class PlaceNail {
private:
    speed placeRate;
    speed retractRate;
public:
    PlaceNail(std::vector<std::string> segments);

    std::string Rebuild();
};


#endif //STRINGARTROBOT_PLACENAIL_H
