from currentTime import *
from writeToFile import *

'''
Course()
    - stores sessions' name, time, info, and days
    - a new instance of the course class is initialized when the user calls .addclass
'''
class Course():
    def __init__(self, name : str, days : list, scheduledTime : str, info : str):
        self.name = name
        self.time = scheduledTime
        self.info = info
        self.days = days

'''
User()
    - stores the user's information provided by discord such as the id, name, and mention
    - a new instance of the user class is initialized when a new user is detected
    - each user has an array of sessions to store their classes
    - the sessions class stores the datatype of course()

addClass()
    - append a new session into sessions
'''
class User():
    def __init__(self, id : int, name, mention):
        self.id = id
        self.name = name
        self.mention = mention
        self.sessions = []
    
    def addClass(self, course : Course):
        self.sessions.append(course)

'''
autoFilter()
    - organize the data that is entered by the user
    - calls the schedule function to officially schedule the session for the user
'''
def autoFilter(rawClassName, rawStartTime, rawActiveDays, notes, author):
    wordsInClassName = rawClassName.split("_")     #Create spaces from "_" for the classNames Ex: Calculus_3_Multivariable -> Calculus 3 Multivariable
    className = ""
    for word in wordsInClassName: #since wordInClassName is a list, we want the class name to be a string
        className = className + word + " "

    #Put the days of the week into a list
    activeDays = rawActiveDays.split(",")
    filteredStartTime = rawStartTime.split(":")
    
    return schedule(className, filteredStartTime, activeDays, notes, author)

'''
checkDateFormat()
    - checks if the user has entered the date and time correctly
    - if day should match with one of the following entries provied in "validDays"
    - the time should follow a 24hr convention:
        hour hand should be between 0-24
        minute hand should be between 0-59
    - if any of the above is violated, return an error message
'''
def checkDateFormat(startTime : list, days : list):
    for day in days: #Check to make sure the user has entered a correct date
        day = str(day).lower()
        if day not in validDays:
            return "The days are not formatted correctly"

    if int(startTime[0]) < 0 or int(startTime[0]) > 24: #The first element in the list stored the hour
        return "Time cannot be negative or over the value of 24 for the hour"
    
    elif int(startTime[1]) < 0 or int(startTime[1]) > 59: #The second element in the list stored the minute
        return "Time cannot be negative or over the value of 59 for the minute"

'''
schedule()
    - function checks if the date and the time are correct, if not return the error message
    - create a new instance for the new sessions
    - add the new session to the user
'''
def schedule(className, startTime : list, days : list, notes, author):
    errorMessage = checkDateFormat(startTime, days)
    if errorMessage != None: return errorMessage

    time = str(startTime[0] + ":" + startTime[1]) #Change the time back to the regular format

    newCourse = Course(className, days, time, notes) #create a new instance of course() to store the new session

    if userInFile(author.id): #If it is a existing user, append the new course to their profile
        for user in users: #look for that user's class in the array of users
            if str(author.id) == str(user.id): #if user class is found
                user.addClass(newCourse) #append the session to the user's profile
                save(user, newCourse, False) #save to json file
                return

    else: #A new user
        newUser = User(author.id, author, author.mention) #creata new instance of user()
        newUser.addClass(newCourse) #append the session
        users.append(newUser) #add that user to the bot's memory

        save(newUser, newCourse, True) #save to json file
        return

'''
load()
    - once a user calls .load, the bot will look thru the json file to find the user
    - if the user is found, it will create a new instance of the user() and store it into the bot's memory
    - the bot will grab all the sessions belong to the user to its memory for easy access
    - this was setup to prevent the bot from losing all data after it goes offline
'''
def load(userID : int, mention):
    logs = readJsonFile() #get the current data from users.json

    for member in logs:
        if int(member["id"]) == userID: #if the bot found the user
            newUser = User(userID, member["name"], mention) #create a new instance of user()
            users.append(newUser) #add the user to the list
            for session in member["sessions"]: #look thru the user's sessions
                newCourse = Course(session["name"], session["days"], session["time"], session["info"])
                newUser.addClass(newCourse) #append them all into sessions

'''
userInFile()
    - checks to see if an user exist in the json file
    - returns true if a user exist in file and false if not
'''
def userInFile(userID : int):
    logs = readJsonFile()

    for member in logs:
        if int(member["id"]) == userID:
            return True
    
    return False

users = [] #list of all users