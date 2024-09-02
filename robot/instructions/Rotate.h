//
// Created by Quintin Dunn on 9/2/2024.
//
#include "robot.h"

#include <vector>
#include <string>

#ifndef STRINGARTROBOT_ROTATE_H
#define STRINGARTROBOT_ROTATE_H


// ROT d<direction> a<degrees> s<speed>
class Rotate : public Command {
private:
    tool_id id;
    int direction;
    angle degrees;
    speed rate;
public:
    explicit Rotate(std::vector<std::string>);

    void execute() override;

    std::string Rebuild();
};


#endif //STRINGARTROBOT_ROTATE_H
