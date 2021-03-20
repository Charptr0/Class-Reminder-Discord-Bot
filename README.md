# Class-Reminder-Discord-Bot<img src="https://i.imgur.com/yVf2J2l.png" width="100px" align="right"></img>

<p>The purpose of this bot is to remind students when their class is about to begin. A user profile will be initialized when they have added a class using the <code>.addclass</code> command. The bot will check its memory every sixty seconds. If the bot finds a class that matches the current time and the date, it will ping the appropriate user and display an embed message containing:
  <ul color="blue"><img src="https://i.imgur.com/gOEM3NS.png" width="300px" height="100%" align="right"></img>
    <li>Title</li>
    <li>Description</li>
    <li>Class Name</li>
    <li>Time</li>
    <li>Link/Info</li>
    <li>Footer Message</li>
  </ul>
</p>

<p>If the user wishes to remove a class or themeslves from the bot's database, they could simply use the <code>.removeclass</code> or the <code>.removeme</code> command.
</p>

<h2>Commands</h2>
<p><em>For a list of all commands, please check the <strong>commands.md</strong> file or click <a href="https://github.com/ptrChar/Class-Reminder-Discord-Bot/blob/master/commands.md">here</a></em></p>

<h2>Backup System</h2> <img src="https://i.imgur.com/bvDlJNO.png" width="120px" height="100%" align="right"</img>
<p>The user.json file stores the profile of all its users. This file includes the user's discord name, ID, and sessions. The sessions are stored as a list of dictionaries that contain the class name, time, days, and info. If the bot gets disconnected from the server or gone offline, the user can simply use the <code>.loadme</code> command to reload their profile back once the admin has restarted the bot.</p>

<p>This backup system was implemented to help the user get their profile back as fast as possible. Without it, once the bot has gone offline, it will lose all its data in its memory. By having a separate file to log all the data, it makes it convenient for the user and the server's admin.</p>




<h2>Installation</h2>

<div><strong>The Basics</strong>
<ol>
  <li>Create a <a href="https://discord.com/">discord account</a></li>
  <li>Create an empty bot from the <a href="https://discord.com/developers/applications">Discord Developer Portal</a></li>
  <li>Invite the empty bot to your server</li>
</ol>
</div>

<div><strong>Starting the bot</strong>
<ol>
  <li>Clone this repository</li>
  <li>Copy your bot token and paste it into the token variable (The token has to be a string)</li>
  <li>Copy your ID from discord and paste it into the adminID variable (This allows you to use admin commands)</li>
</ol>
</div>

<h2>Tech</h2>
<ul>
  <li>Discord API</li>
  <li>PYTZ</li>
</ul>


