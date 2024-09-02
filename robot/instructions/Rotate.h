//
// Created by Quintin Dunn on 9/2/2024.
//
#include "robot.h"

#include <vector>
#include <string>

#ifndef STRINGARTROBOT_ROTATE_H
#define STRINGARTROBOT_ROTATE_H


// ROT d<direction> a<degrees> s<speed>
class Rotate {
private:
    int direction;
    angle degrees;
    speed rate;
public:
    Rotate(std::vector<std::string>);
    ~Rotate() = default;

    std::string Rebuild();
};


#endif //STRINGARTROBOT_ROTATE_H
