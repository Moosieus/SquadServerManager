"""
All file paths must use two \\ to mark folders. Trust me, it's just easier this way.
"""

"""GENERAL INFO"""

ftp_path = "/"

ftp_ip = 'squad.stratumservers.com'
ftp_port = 2022

server_ip = '204.12.216.98'
query_port = 27165

ftp_user = 'wjr6phxy.96229838'
ftp_passwd = '*:QyULy766Ca0z'

if ftp_ip is '':
    ftp_ip = server_ip

local_path = '.\\FTP_FILES'
"""DISCORD SETTINGS"""

call_string = '!'  # The discord bot will only respond to messages that start with these characters.
admin_file = 'Admins.cfg' # The name of the discord admins file.

vote_channel_id = 483747819656839169

vote_channel_header = "**VOTEMAP: **```Our server has a vote map system! At the start of each round, you will be able "\
+ "to vote for 3 different layers using the '!vote 1', '!vote 2', or '!vote 3' commands. "\
+ "Donors Silver or above will have their votes weighted at 2x. You only get one vote and it's not reversible, so choose wisely!```*Images provided by http://squadmaps.com*"

rules_broadcasts = [
    'All SL\'s must use mics. Don\'t abuse chat.',
    'Do not make squads and leave them. Apologize for all TK in all.',
    'Don\'t shoot at enemy main base protection zones.',
    'Full rules and vote for next map @ discord.me/sna'
]

premium_vote_roles = ['482579186905645085', '482579401863725086', '482579709226647570'] # Silver Gold Platinum

"""
You must create your own Discord bot to use this program.
https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
Do not share your bot token with others. Doing so would allow bad actors to take control
of the bot's identity, and potentially use it to run their own malicious code.
"""
bot_token = 'NDgzNjU0MTIyNTI5MjI2NzU1.DmWnGg.qOqvcTngMYmlzXf0h65w5NFFwbg'  # Bring Your Own Bot.

"""
For a layer of safety, you must provide the bot with the ID's of the servers and channels it sends debug messages to.
To get a server or channel ID, go to your User Settings > Appearance > Enable Developer Mode.
Then simply right click on the server or channel, and click "Copy ID".
Warning: Using too many debug channels may cause an overflow. 
"""
debug_channels = ['459403329089437732']

"""Also don't forget to add administrators in the Admins.cfg file!"""
