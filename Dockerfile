FROM python:3.8

WORKDIR /class_reminder_bot

# Install Dependencies 
RUN pip install discord
RUN pip install pytz 

#Copy the local folder to the WORKDIR folder
COPY . .

#Start the bot
CMD [ "python", "bot_main.py" ]