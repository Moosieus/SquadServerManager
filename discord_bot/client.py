import discord as dis
from fuzzywuzzy import fuzz
from squad_rcon.commands import commands
from server_config import call_string, debug_channels
import re
from miscellaneous.misc import is_steamid64, str_to_epoch, epoch_from_now
from discord_bot.parse_channel_file import *


def scrub_input(content):
    """Converts message content to string, removes call characters, and mono-spaces the message."""
    return re.sub(r'\s+', ' ', str(content)[len(call_string):])


"""BOT FUNCTIONS"""


async def debug_message(self, message_string):
    """Sends a message to all user designated debug channels."""
    for channel_id in debug_channels:
        channel = self.client.get_channel(channel_id)
        await self.client.send_message(channel, message_string)


async def validate_channels(self):
    """Checks to see if all debug channels are usable. Unusable channels are removed from debug channels."""
    failed = []
    for channel_id in debug_channels:
        channel = self.client.get_channel(channel_id)
        if channel is None:
            failed.append((channel_id, 'does not exist.'))
        elif channel.type is not dis.ChannelType.text:
            failed.append((channel_id, 'is not a text channel.'))
        else:
            permissions = channel.permissions_for(channel.server.get_member(self.client.user.id))
            if permissions.read_messages is False or permissions.send_messages  is False:
                failed.append((channel_id, 'cannot read or send messages.'))
    for c in failed:
        debug_channels.remove(c[0])
    if len(failed) == 0:
        await self.func['debug_message'](self, 'All debug channels are accessible.')
    else:
        await self.func['debug_message'](
            self,
            'The bot was unable to use the channels with the following ID\'s on startup: \n' + '\n'.join([f"{i[0]}, {i[1]}" for i in failed]) + '\nThese channels will not be used for debug messages.'
        )

"""COMMANDS"""


# ...setban steamid64 0M the rest of this is a comment.
async def set_ban(self, last_message):
    """Edits a users ban in the bans.cfg file."""
    content = scrub_input(last_message.content)
    content = content.split(' ', 3)
    steamid64 = content[1]
    if is_steamid64(steamid64):
        if content[2].lower() == 'remove':
            self.server.set_ban(steamid64, remove=True)
        else:
            if content[2] == '0':
                time_stamp = 0
            else:
                time_stamp = epoch_from_now(
                    str_to_epoch(content[2])
                )
            self.server.set_ban(
                steamid64,
                time_stamp=time_stamp,
                ds_comment=content[3] if len(content) >= 4 else ''
            )
        await self.client.send_message(last_message.channel, 'Ban Updated.')
    else:
        await self.client.send_message(last_message.channel, 'Error: Invalid SteamID.')


# ...get_ban steamid64
async def get_ban(self, last_message):
    """Searches for a steamid in the bans.cfg file and returns the relevant information."""
    content = scrub_input(last_message.content)
    content_list = content.split(' ')
    steamid64 = content_list[1]
    if is_steamid64(steamid64):
        response = self.server.is_banned(steamid64)
        await self.client.send_message(last_message.channel, response)
    else:
        await self.client.send_message(last_message.channel, 'Error: Must use a steamid64 user ID.')


# ...help
async def help(self, last_message):
    """Displays a Markdown help sheet for the bot."""
    await self.client.send_message(last_message.channel, f'```md\n' + open('bot help.md', 'r').read() + '```')


# ...ListPlayers
async def rcon(self, last_message):
    """Passes the command to the rcon client, and returns the message from the server_scripts."""
    content = scrub_input(last_message.content)
    rcon_reply = await self.rcon.send_command(content)
    await self.client.send_message(last_message.channel, rcon_reply)

"""ADMIN CONTROL"""


# ...MakeAdmin userID comment
async def make_admin(self, last_message):
    """Adds a user to the Admins.cfg file."""
    content = scrub_input(last_message.content).split(' ', 2)
    try:
        append_admin(content[1], comment=content[2])
        self.admins = parse_admins()
        await self.client.send_message(last_message.channel, 'User added to discord admins.')
    except Exception as e:
        await self.client.send_message(last_message.channel, f'Error: {e.args[0]}')


# ...RemoveAdmin userID
async def remove_admin(self, last_message):
    """Removes a user fro mthe Admins.cfg file."""
    content = scrub_input(last_message.content).split(' ', 1)
    try:
        remove_admin(content[1])
        self.admins = parse_admins()
    except Exception as e:
        await self.client.send_message(last_message.channel, f'Error: {e.args[0]}')
    self.admins = parse_admins()


# ...RefreshAdmins
async def refresh_admins(self):
    self.admins = parse_admins()

"""BASE ROUTINE"""

async def standby(self):
    """ The default state of the bot, loops back after every command. Matches message to defined routines."""
    @self.client.event
    async def on_message(message):
        if message.author.id != self.client.user.id and message.author.id in self.admins:
            if str(message.content).startswith(call_string):
                self.client.send_message(message.channel, 'Entering standby routine.')
                command = str(message.content).split(' ', 1)[0]
                best_ratio = ('', 0)
                for rout in self.routines:
                    ratio = fuzz.token_sort_ratio(command, rout) # was partial_ratio
                    if ratio > best_ratio[1]:
                        best_ratio = (rout,ratio)
                if best_ratio[1] > 50:
                    print(f'{best_ratio[0]}, {best_ratio[1]}')
                    await self.routines[best_ratio[0]](self, last_message=message)
                else:
                    await self.client.send_message(message.channel, 'Failed to interpret command. (Match < 50)')


"""BOT CLASS"""


class ServerBot:
    """ A class built on top of the discord.py client to handle discord functionality."""
    client = dis.Client()  # type: dis.Client

    routines = { # Stores every function for the discord bot and maps it to a keyword.
        **{k:rcon for k in commands}, # Adds all rcon commands to the routine dict, maps them to rcon command.
        'standby': standby,
        'help': help,
        'getban': get_ban,
        'setban': set_ban,
        'MakeAdmin': make_admin,
        'RemoveAdmin': remove_admin,
        'RefreshAdmins': refresh_admins
    }  # type : dict

    admins = parse_admins()

    func = {
        'debug_message': debug_message
    }

    def __init__(self, rcon, server_parser):
        """ Initialize and run the bot."""
        self.rcon = rcon
        self.server = server_parser
        @self.client.event
        async def on_ready():
            print('Logging in as: ' + self.client.user.name)
            print('With user ID: ' + self.client.user.id)
            rout = self.routines['standby']

            await validate_channels(self)
            await rout(self)
