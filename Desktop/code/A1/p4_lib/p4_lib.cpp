#include <iostream>
#include <utility>
#include <vector>
#include "p4_lib.h"
#include <map>

//returns whether date1 comes before date2
bool date_is_before(std::pair<int, int> date1, std::pair<int, int> date2) {

    //if date1 month is before date2 month, return true
    if (date1.first < date2.first) {
        return true;
    }

    //if both months are the same, check days
    if (date1.first == date2.first) {
        if (date1.second < date2.second) {
            return true;
        }
        else {
            return false;
        }
    }

    //if true has not been returned, return false
    return false;
}

//returns how many days are in a given month
int days_in_month(int month) {
    std::map<int, int> dates = {{1, 31},
                                {2, 28},
                                {3, 31},
                                {4, 30},
                                {5, 31},
                                {6, 30},
                                {7, 31},
                                {8, 31},
                                {9, 30},
                                {10, 31},
                                {11, 30},
                                {12, 31}};

    return dates[month];
}

//returns the new date given a first date plus an amount of days forward
std::pair<int, int> date_plus(std::pair<int, int> date, int days_forward) {
    
    // adds days forward to inital date
    int day = date.first + days_forward;
    int month = date.second;

    //if the new amount of days exceeds the total amount of days within the month, add months until appropriate
    //subtract days in month from total day for current day
    while (day > days_in_month(month)) {
        month++;
        day = day - days_in_month(month);
    }

    //return new date
    std::pair<int, int> new_date(month, day);
    return new_date;
}

std::pair<int, int> latest_date(std::vector<std::pair<int, int>> list_of_dates) {
    
}
