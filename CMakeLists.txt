cmake_minimum_required(VERSION 3.29)
project(StringArtRobot)

set(CMAKE_CXX_STANDARD 14)

include_directories(robot)

add_executable(StringArtRobot
    robot/robot.cpp
    robot/robot.h
        robot/main.cpp
        robot/utils/string_utils.cpp)
