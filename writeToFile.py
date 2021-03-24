import json

'''
readJsonFile()
    - read and import the contents from users.json
    - return the content of the file
'''
def readJsonFile():
    with open("users.json", "r") as f:
        logs = json.load(f)
    
    return logs

'''
writeJsonFile()
    - dump the contents stored in "logs" into users.json
'''
def writeJsonFile(logs):
    with open("users.json", "w") as f:
        json.dump(logs, f, indent=2)

'''
save()
    - once a user has added a class, the function checks to see if it is a new user or not
    - if newUser, add the user's name, id, and sessions to file
    - if not, the bot will find the user in the json file, then append the new session
'''
def save(user, course,  newUser : bool): #Save the user's config
    logs = readJsonFile() #get the current data from users.json

    if newUser: #Create a new player profile
        logs.append({
            "name" : str(user.name),
            "id" : str(user.id),
            "sessions" : [{
                "name" : course.name,
                "time" : course.time,
                "days" : course.days,
                "info" : course.info
            }
            ]
        })

    else: #Existing user
        for member in logs:
            if str(member["id"]) == str(user.id): #Find the user using their discord id
                member["sessions"].append({
                    "name" : course.name,
                    "time" : course.time,
                    "days" : course.days,
                    "info" : course.info
                })

    writeJsonFile(logs) #save the changes

'''
removeClassFromFile()
    - remove a class from a user in the json file
'''
def removeClassFromFile(userID : int, className): #Remove a class from the json file
    logs = readJsonFile() #get the current data from users.json

    for member in logs:
        if int(member["id"]) == userID: #find the user
            for session in member["sessions"]: #loop thru all the sessions that the user have on file
                if className in session["name"]:  #if the intended class was found
                    member["sessions"].remove(session) #Delete the entry

    writeJsonFile(logs) #save the changes

'''
removeUserFromFile()
    - remove a user from user.json
'''
def removeUserFromFile(userID : int):
    logs = readJsonFile() #get the current data from users.json

    for member in logs:
        if int(member["id"]) == userID: #if a user's id matches an id in the logs, remove the user
            logs.remove(member)
    
    writeJsonFile(logs) #save the changes