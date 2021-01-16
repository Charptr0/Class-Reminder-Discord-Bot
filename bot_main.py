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
    embed.set_footer(text="If you encounter any problems with the bot, please report it to " + str(bot.get_user(adminID)))
    return embed

@bot.event
async def on_ready():
    print("The bot is ready")

@bot.command("addclass")
async def addClass(ctx, className : str, startTime : str, days : str, *, notes : str):
    errors = ClassScheduler.autoFilter(className, startTime, days, notes, ctx.author)
    #If return "None", then the format is correct
    if errors == None:
        await ctx.send("Success! The class has been added to your profile")
    #If not display the error message
    else:
        await ctx.send(errors)

@bot.command("start") #Start the reminder
@commands.check(adminCheck)
async def start(ctx): #Start the loop
    global mainChannel
    mainChannel = int(ctx.channel.id)
    reminder.start()

@bot.command("stop") #Stop the reminder
@commands.check(adminCheck)
async def stop(ctx):
    reminder.stop() #Stop the loop
    await ctx.send("The bot has stopped")

@bot.command("reset") #A factory reset, admin perms only
@commands.check(adminCheck)
async def factoryReset(ctx): #Destroy all data 
    ClassScheduler.users.clear()
    await ctx.send("A database reset has been complete")

@tasks.loop(seconds=10)
async def reminder():
    currentTime = getCurrentTime()[:-3] #Get the time
    currentDay = getCurrentDay() #Get the day 

    channel = bot.get_channel(mainChannel)
    for user in ClassScheduler.users:
        if bot.get_user(user.id) == None: #If the user left the server
            continue
        for course in user.sessions:
            if currentDay in course.days and currentTime in course.time: #If a session is found, alert the user with a ping
                embedMsg = createEmbed(course)
                await channel.send(user.name.mention + ", one of your class is about to start or it's starting right now")
                await channel.send(embed=embedMsg)
    
@bot.command("removeme") #Remove the user completely 
async def removeMe(ctx):
    for user in ClassScheduler.users:
        if ctx.author.id == user.id:
            ClassScheduler.users.remove(user)
            ClassScheduler.removeUserFromFile(ctx.author.id)
            await ctx.send(str(ctx.author.mention) + " has been deleted")
            return

    await ctx.send("You are not in the database")

@bot.command("loadme") #If the bot goes offline, all data will be lost, this commands help bring the user's data back
async def loadMeFromBackUp(ctx):
    try:
        ClassScheduler.load(ctx.author.id)
        await ctx.send("Success, your profile has been loaded")
    except:
        await ctx.send("Could not find your profile in system, load failed")

@bot.command("removeclass") #Remove a class from the json file and from the current cache
async def removeClass(ctx, * , className : str):
    for user in ClassScheduler.users:
        if int(ctx.author.id) == user.id:
            for course in user.sessions:
                if className in str(course.name):
                    user.sessions.remove(course)
                    ClassScheduler.removeClassFromFile(ctx.author.id, className)
                    await ctx.send("You have sucessfully removed " + str(className))
                    return
    
    await ctx.send("An error has occured, please contact " + str(bot.get_user(adminID)))

@bot.command("checkme") #A quick way to see all the user's classes
async def checkMe(ctx):
    for user in ClassScheduler.users:
        if int(ctx.author.id) == user.id: #If the player is in the database
            await ctx.send(str(ctx.author.mention))
            for course in user.sessions:
                await ctx.send(str(course.name) + "\t" + str(course.time) + "\t" + str(course.days) + "\t" + str(course.info))

bot.run(token) #Run the bot