from currentTime import *
from writeToFile import *

class Course():
    def __init__(self, name : str, days : list, scheduledTime : str, info : str):
        self.name = name
        self.time = scheduledTime
        self.info = info
        self.days = days

class User():
    def __init__(self, id : int, name, mention):
        self.id = id
        self.name = name
        self.mention = mention
        self.sessions = []
    
    def addClass(self, course : Course):
        self.sessions.append(course)

def autoFilter(rawClassName, rawStartTime, rawActiveDays, notes, author):
    #Create spaces from "_" for the classNames Ex: Calculus_3_Multivariable -> Calculus 3 Multivariable
    wordsInClassName = rawClassName.split("_") 
    className = ""
    for word in wordsInClassName:
        className = className + word + " "

    #Put the days of the week into a list
    activeDays = rawActiveDays.split(",")
    filteredStartTime = rawStartTime.split(":")
    
    return schedule(className, filteredStartTime, activeDays, notes, author)

def checkDateFormat(startTime : list, days : list):
    for day in days: #Check to make sure the user has entered a correct date
        day = str(day).lower()
        if day not in validDays:
            return "The days are not formatted correctly"

    if int(startTime[0]) < 0 or int(startTime[0]) > 24: #The first element in the list stored the hour
        return "Time cannot be negative or over the value of 24 for the hour"
    
    elif int(startTime[1]) < 0 or int(startTime[1]) > 59: #The second element in the list stored the minute
        return "Time cannot be negative or over the value of 59 for the minute"

   
def schedule(className, startTime : list, days : list, notes, author):
    errorMessage = checkDateFormat(startTime, days)
    if errorMessage != None: return errorMessage

    time = str(startTime[0] + ":" + startTime[1]) #Change the time back to the regular format

    newCourse = Course(className, days, time, notes)

    if userInFile(author.id):
        for user in users: #If it is a existing user
            if str(author.id) == str(user.id):
                user.addClass(newCourse)
                save(user, newCourse, False)
                return

    else: #A new user
        newUser = User(author.id, author, author.mention)
        newUser.addClass(newCourse)
        users.append(newUser)

        save(newUser, newCourse, True)
        return

def load(userID : int, mention):
    logs = readJsonFile()

    for member in logs:
        if member["id"] == userID:
            newUser = User(userID, member["name"], mention)
            users.append(newUser)
            for session in member["sessions"]:
                newCourse = Course(session["name"], session["days"], session["time"], session["info"])
                newUser.addClass(newCourse)

def userInFile(userID : int):
    logs = readJsonFile()

    for member in logs:
        if int(member["id"]) == userID:
            return True
    
    return False

users = []