import json

def readJsonFile():
    with open("users.json", "r") as f:
        logs = json.load(f)
    
    return logs

def writeJsonFile(logs):
    with open("users.json", "w") as f:
        json.dump(logs, f, indent=2)

def save(user, course,  newUser : bool): #Save the user's config
    logs = readJsonFile()

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

    writeJsonFile(logs)

def removeClassFromFile(userID : int, className): #Remove a class from the json file
    logs = readJsonFile()

    for member in logs:
        if int(member["id"]) == userID: 
            for session in member["sessions"]:
                if className in session["name"]:
                    member["sessions"].remove(session) #Delete the entry

    writeJsonFile(logs)


def removeUserFromFile(userID : int):
    logs = readJsonFile()

    for member in logs:
        if int(member["id"]) == userID:
            logs.remove(member)
    
    writeJsonFile(logs)