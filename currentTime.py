import datetime
import pytz

dateDict = {
    0 : "mon",
    1 : "tue",
    2 : "wed",
    3 : "thru",
    4 : "fri",
    5 : "sat",
    6 : "sun",
    "mon" : 0,
    "tue" : 1,
    "wed" : 2,
    "thru": 3,
    "fri" : 4,
    "sat" : 5,
    "sun": 6
}

validDays = ["mon", "tue", "wed", "thru", "fri", "sat", "sun"]

def getRawTime():
    return datetime.datetime.now(tz= pytz.UTC).astimezone(pytz.timezone("US/Eastern")) #Grab the current date, and time  

def getCurrentTime():
    rawTime = getRawTime()
    return str(rawTime.time())[:8] #Return only the time in hr:min:sec form  

def getCurrentDay():
    rawTime = getRawTime()
    return str(dateDict[rawTime.weekday()]) #Return only the day of the week

def getCurrentDate():
    rawTime = getRawTime()
    return str(rawTime.date()) #Return only the date in year-month-day form
