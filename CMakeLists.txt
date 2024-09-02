cmake_minimum_required(VERSION 3.29)
project(StringArtRobot)

set(CMAKE_CXX_STANDARD 20)

include_directories(robot)

add_executable(StringArtRobot
    robot/robot.cpp
    robot/robot.h
        robot/main.cpp
        robot/utils/string_utils.cpp
        robot/instructions/Rotate.cpp
        robot/instructions/Rotate.h
        robot/instructions/instructions.h
        robot/instructions/PlaceNail.cpp
        robot/instructions/PlaceNail.h
        robot/instructions/Beep.cpp
        robot/instructions/Beep.h
        robot/instructions/Sleep.cpp
        robot/instructions/Sleep.h
)
