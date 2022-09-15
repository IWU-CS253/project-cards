#Returns true if date1 comes before date2
def date_is_before(date1 , date2):

    #date[0] would be the month
    if date1[0] < date2[0]:
        return True
    
    #if the months are the same, check for the dayes
    if date1[0] == date2[0]:
        if date1[1] < date2[1]:
            return True
        else:
            return False
    
    #if true has not been returned, return false
    return False


def days_in_month(month):

    months = {1: 31,
              2: 28, 
              3: 31, 
              4: 30, 
              5: 31, 
              6: 30, 
              7: 31, 
              8: 31, 
              9: 30, 
              10: 31, 
              11: 30, 
              12: 31}

    return(months[month])


#returns the date of the given date plus amount of days forward
def date_plus(date, days_forward):

    #adds days forward to day in date
    day = date[1] + days_forward
    month = date[0]
    
    #if the day is greater than the total amount of days in the month, add months until the desired month is reached
    # subract the day from how many days there are in the month for current day
    while day > days_in_month(month):
        month = month + 1
        day = day - days_in_month(month)
    
    #return new date
    new_date = (month, day)
    return new_date

#returns the latest date given a list of dates
def latest_date(list_of_dates):
    dates = list(enumerate(list_of_dates))
    latest = ((date[0] for date in dates))
    #for i in dates:
    #    if date_is_before(latest, dates.index(dates[i])) == False:
    #        latest = dates.index(dates[i])
    
    print(latest)
