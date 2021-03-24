<h1><strong>All available commands</strong></h1>


<h2>Admin Commands</h2>
<code>.start</code>
<p>This command takes no arguments, it will start the background loop. In order for the bot to start sending out reminder messages, 
this command <strong>need</strong> to be called. </p>

<code>.stop</code>
<p>This command takes no arguments, it will stop the background loop.</p>

<code>.reset</code>
<p>This command takes no arguments, it do a factory reset of the bot, removing every single member from memory and the JSON file.</p>

<h2>All Commands</h2>

<code>.addclass [class name] [time] [days of the week] [info/link]</code>
<p>This commands will add a class to the user's profile. It takes 4 arguments:</p>
<ol>
  <li>The class name. (No spacing) | Ex: Math 391-> Math_391, Physics 208 Lab -> Physics_208_Lab</li>
  <li>The time when the class starts | Ex: 3pm -> 15:00, 10am -> 10:00, 7:30-> 19:30</li>
  <li>The days of the week when the classes is in session | Ex: Monday and Tuesday -> mon,tue | Ex: Thrusday and Friday -> thru,fri
  <li>The user can put anything they want in here
</ol>

<code>.removeclass [class name] </code>
<p>This command will remove a class from the user's profile.</p>
<p> NOTE: The class name has to be spaced | Example: Math_391 -> Math 391</p>

<code>.removeme</code>
<p>This command takes no arguments, it will remove the user from the memory and the JSON file</p>

<code>.checkme</code>
<p>This command takes no arguments, the bot will send the user all their info and classes that is inside their profile</p>

<code>.loadme</code>
<p>This command takes no arguments. If the bot ever goes offline, once it has reconnected, users can use this command the reload their profile from the JSON file (AKA a backup system)</p>

