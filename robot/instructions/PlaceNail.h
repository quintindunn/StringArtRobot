//
// Created by Jason on 9/2/2024.
//

#ifndef STRINGARTROBOT_PLACENAIL_H
#define STRINGARTROBOT_PLACENAIL_H

#include "robot.h"
#include "instructions.h"

#include <string>
#include <vector>

class PlaceNail : public Command{
private:
    speed placeRate;
    speed retractRate;
public:
    explicit PlaceNail(std::vector<std::string> segments);

    void execute() override;

    std::string Rebuild();
};


#endif //STRINGARTROBOT_PLACENAIL_H
