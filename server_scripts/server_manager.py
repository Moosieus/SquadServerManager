from squad_rcon.rcon import SquadRconClient
from discord_bot.client import ServerBot
from steam.game_servers import a2s_info
from server_config import *
import asyncio, time
from miscellaneous.random_layer_generator import generate_layer_list
from server_scripts.vote_map import VoteMap
from server_scripts.server_file_parser import SquadFileUtils

from server_config import vote_channel_id
from discord_bot.client import init_voting_channel


class ServerManager:
    """Handles all inputs, data sources, and behaviors."""
    def __init__(self):
        print("Initializing Server Manager...")
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.server_files = SquadFileUtils()
        print("Loaded Squad file utils.")
        self.loop.run_until_complete(self.create_rcon())
        if type(self.server_files.sq_ftp) is not bool:
            self.tasks.append(self.server_files.sq_ftp.keep_alive)

        if self.rcon_dict['Password'] == "":
            print("RCON is not enabled in Rcon.cfg (no password).")
            exit()

        self.rcon = SquadRconClient(
            self.rcon_dict['IP'],
            self.rcon_dict['Port'],
            self.rcon_dict['Password']
        )
        
        self.vote_map = VoteMap(self.rcon, generate_layer_list, a2s_info((server_ip, query_port))['map'])
        self.loop.run_until_complete(self.vote_map.evaluate_votes())
        self.discord = ServerBot(self.rcon, self.server_files, self.vote_map)
        self.tasks.append(self.broadcast_rules)
        self.last_layer = a2s_info((server_ip, query_port))['map']
        self.last_broadcast = round(time.time())
        """ASYNC LOOP"""
        try:
            self.loop.run_until_complete(
                asyncio.wait(
                    [self.discord.client.start(bot_token)] +
                    [asyncio.ensure_future(f()) for f in self.tasks]
                )
            )
        except KeyboardInterrupt:
            # This code only works after an error has occurred...
            print("KB Interput")
            self.loop.run_until_complete(self.discord.client.logout())
            pending = asyncio.Task.all_tasks(loop=self.loop)
            gathered = asyncio.gather(*pending, loop=self.loop)
            try:
                gathered.cancel()
                self.loop.run_until_complete(gathered)
                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except:
                pass
        finally:
            self.loop.close()

    async def create_rcon(self):
        self.rcon_dict = await self.server_files.get_rcon_info()

    async def broadcast_rules(self, interval=5):
        if self.last_layer != a2s_info((server_ip, query_port))['map']:
            print('NEW ROUND STARTED')
            print('BROADCAST FOR NEW ROUND')
            [await self.rcon.send_command(f'broadcast {msg}') for msg in rules_broadcasts]
            print("RULE BROADCAST SUCCESSFUL")
            await asyncio.sleep(1)
            self.last_layer = a2s_info((server_ip, query_port))['map']
            self.last_broadcast = round(time.time())
            self.vote_map.reinit(self.last_layer)
            await self.vote_map.evaluate_votes()
            await init_voting_channel(self.discord, vote_channel_id)

        elif round(time.time())-(60*20) > self.last_broadcast:
            print('BROADCAST FOR TIME DELTA')
            [await self.rcon.send_command(f'broadcast {msg}') for msg in rules_broadcasts]
            await asyncio.sleep(1)
            self.last_broadcast = round(time.time())

        else:
            await asyncio.sleep(interval)
        await self.broadcast_rules()
