import discord
from discord import embeds
from currentTime import getCurrentDay, getCurrentTime
from discord.ext import commands, tasks
import ClassScheduler

token = "" #Put your tokens here

mainChannel = None
adminID = int()

bot = commands.Bot(command_prefix= ".")
def adminCheck(ctx):
    return ctx.author.id == adminID

def createEmbed(course): #Creating that fancy message
    embed = discord.Embed(title="A Class Reminder", description="A class is starting", colour=discord.Colour.blue())
    embed.add_field(name="Class Name", value=course.name, inline=False)
    embed.add_field(name="Time", value=course.time, inline=False)
    embed.add_field(name="Link/Info", value=course.info, inline=False)
    embed.set_footer(text="If you encounter any problems with the bot, please report it to the mods")
    return embed

@bot.event
async def on_ready():
    print("The bot is ready")

'''
addclass()
    - alllow the user to add a class for the bot to remind
    - must provide the class name, days, start time, and notes if nesscary
    - the bot will send the user a message if it has successfully executed the command
'''
@bot.command("addclass")
async def addClass(ctx, className : str, startTime : str, days : str, *, notes : str):
    errors = ClassScheduler.autoFilter(className, startTime, days, notes, ctx.author)
    #If return "None", then the format is correct
    if errors == None:
        await ctx.send("Success! The class has been added to your profile")
    #If not display the error message
    else:
        await ctx.send(errors)

'''
start()
    - start the background loop, the bot will check its database every 60s
'''
@bot.command("start") #Start the reminder
@commands.check(adminCheck)
async def start(ctx): #Start the loop
    global mainChannel
    mainChannel = int(ctx.channel.id)
    reminder.start()
    await ctx.send("The loop has started")

'''
stop()
    - stop the background task
'''
@bot.command("stop") #Stop the reminder
@commands.check(adminCheck)
async def stop(ctx):
    reminder.stop() #Stop the loop
    await ctx.send("The loop has stopped")

'''
reset()
    - factory reset of the bot
    - the bot's memory and database must be wiped
'''
@bot.command("reset") #A factory reset, admin perms only
@commands.check(adminCheck)
async def factoryReset(ctx): #Destroy all data 
    ClassScheduler.users.clear()
    ClassScheduler.reset()

    await ctx.send("A database reset has been complete")

'''
reminder()
    - every 60s, the bot will run this function
    - it will check its database for matching days and time for a class
    - if a matching time and day is found, it will create a embedded message and ping the owner of the class
'''
@tasks.loop(seconds=60)
async def reminder():
    currentTime = getCurrentTime()[:-3] #Get the time
    currentDay = getCurrentDay() #Get the day 

    channel = bot.get_channel(mainChannel)

    for user in ClassScheduler.users:
        for course in user.sessions:
            if currentDay in course.days and currentTime in course.time: #If a session is found, alert the user with a ping
                embedMsg = createEmbed(course)
                await channel.send(user.mention)
                await channel.send(embed=embedMsg)
    
'''
removeme()
    - remove a user from the database and from the bot's memory
    - send back a comfirmation message
'''
@bot.command("removeme") #Remove the user completely 
async def removeMe(ctx):
    for user in ClassScheduler.users:
        if ctx.author.id == user.id:
            ClassScheduler.users.remove(user)
            ClassScheduler.removeUserFromFile(ctx.author.id)
            await ctx.send(str(ctx.author.mention) + " has been deleted")
            return

    await ctx.send("You are not in the database")

'''
loadme()
    - if the user is in the database and NOT in the bot's memory, this command should at the user back to memory
    - send back a comfirmation message
'''
@bot.command("loadme") #If the bot goes offline, all data will be lost, this commands help bring the user's data back
async def loadMeFromBackUp(ctx):
    try:
        ClassScheduler.load(ctx.author.id, ctx.author.mention)
        await ctx.send("Success, your profile has been reloaded")
    except:
        await ctx.send("Could not find your profile in system, load failed")

'''
removeclass()
    - remove a class from a user's database
    - send back a comfirmation message
'''
@bot.command("removeclass") #Remove a class from the json file and from the current cache
async def removeClass(ctx, * , className : str):
    for user in ClassScheduler.users:
        if int(ctx.author.id) == int(user.id):
            for course in user.sessions:
                if className in str(course.name):
                    user.sessions.remove(course)
                    ClassScheduler.removeClassFromFile(ctx.author.id, className)
                    await ctx.send("You have successfully removed " + str(className))
                    return
    
    await ctx.send("An error has occurred, please contact the mods")

@bot.command("checkme") #A quick way to see all the user's classes
async def checkMe(ctx):
    for user in ClassScheduler.users:
        if int(ctx.author.id) == user.id: #If the player is in the database
            await ctx.send(str(ctx.author.mention))
            for course in user.sessions:
                await ctx.send(str(course.name) + "\t" + str(course.time) + "\t" + str(course.days) + "\t" + str(course.info))

bot.run(token) #Run the bot