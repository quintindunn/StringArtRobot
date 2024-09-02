//
// Created by Quintin Dunn on 9/2/24.
//


#include <iostream>
#include <locale>
#include <vector>


using std::string;
using std::vector;



vector<string> split(const string& content, const string& delimiter, int count) {
    size_t pos_start = 0, pos_end;
    const size_t delim_len = delimiter.length();
    vector<string> res;

    int i = 0;
    while ((pos_end = content.find(delimiter, pos_start)) != string::npos && (i < count || count == -1)) {
        string token = content.substr(pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back(token);
        i++;
    }

    res.push_back(content.substr(pos_start));
    return res;
}

vector<string> split(const string& content, const string& delimiter) {
    return split(content, delimiter, -1);
}


string toLower(string s) {
    const std::locale loc;
    for(char &c : s)
        c = std::tolower(c, loc);
    return s;
}
