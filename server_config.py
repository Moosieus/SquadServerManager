"""
All file paths must use two \\ to mark folders. Trust me, it's just easier this way.
"""


"""GENERAL INFO"""

server_path = "your\\server\\path\\here"  # Use two \\ instead of one, do not use /
start_file = 'start.bat'  # The name of the start file in your server_path folder. (aka the relative path)
server_ip = 'your.ip.here'  # The public IP this server will use.
server_name = None  # If left as None, the name will be used from "Server.cfg".
steamcmd = 'your\\steamcmd\\executable\\path\\here'  # The path to SteamCMD.

server_appid = 403240  # The app ID of the server client.
client_appid = 393380  # The app ID of the game client.
admin_file = 'Admins.cfg' # The name of the discord admins file.


"""DISCORD SETTINGS"""

call_string = '...'  # The discord bot will only respond to messages that start with these characters.


"""
You must create your own Discord bot to use this program.
https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
Do not share your bot token with others. Doing so would allow bad actors to take control
of the bot's identity, and potentially use it to run their own malicious code.
"""
bot_token = 'YourBotTokenHere'  # Bring Your Own Bot.


"""
For a layer of safety, you must provide the bot with the ID's of the servers and channels it sends debug messages to.
To get a server or channel ID, go to your User Settings > Appearance > Enable Developer Mode.
Then simply right click on the server or channel, and click "Copy ID".
Warning: Using too many debug channels may cause an overflow. 
"""
debug_channels = ['your-channel-id-here']

"""Also don't forget to add administrators in the Admins.cfg file!"""

"""RESTART SETTINGS"""

should_restart = False  # If True, will restart daily (True / False)
restart_hour = 0  # Hour of the day to start (0-23)
restart_minute = 0  # Minute of the hour to restart (0-59)

# Restart warning controls
restart_warn_time = 1  # Minutes to wait after broadcasting restart warning to players
restart_broadcast_message = f'Server is restarting in {restart_warn_time} minute!'

# Restart population watch
wait_for_pop = True  # If True, will wait for player count to drop below threshold to restart (True / False)
restart_pop_delay = 30  # Minutes to wait if server is populated.
restart_pop_threshold = 30  # Waits for server to drop below this population


"""UPDATE SETTINGS"""

should_auto_update = False  # Leave this off for now.
update_broadcast_message = f'A new version of Squad has been released, Go update your game!'
