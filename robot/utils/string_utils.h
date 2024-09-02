//
// Created by Quintin Dunn on 9/2/24.
//

#ifndef STRING_UTILS_H
#define STRING_UTILS_H


#include <vector>
#include <string>

std::vector<std::string> split(const std::string& content, const std::string& delimiter, int count);
std::vector<std::string> split(const std::string& content, const std::string& delimiter);
std::string toLower(std::string);

#endif //STRING_UTILS_H
