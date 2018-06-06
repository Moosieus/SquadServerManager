from steam_scripts.update_listener import UpdateListener
from squad_rcon.rcon import SquadRconClient
from discord_bot.client import ServerBot
from steam.game_servers import a2s_info
from server_scripts.process_info import wait_for_process
from server_config import *
import asyncio, os, time, shutil
from asyncio.subprocess import PIPE, STDOUT
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ServerManager:
    """Handles all inputs, data sources, and behaviors."""
    def __init__(self, server=None):
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.server = server
        self.process = wait_for_process(f"{self.server.path}\\Squad\\Binaries\\Win64\\SquadServer.exe")
        if should_auto_update:
            self.listener = UpdateListener(self.server.get_server_build_time(), self.server.get_client_build_time())
            self.tasks.append(self.update_task)

        if self.server.rcon_pass == "":
            print("RCON is not enabled in Rcon.cfg (no password). Manager cannot run without RCON enabled.")
            exit()

        self.rcon = SquadRconClient(
            self.server.rcon_ip,
            self.server.rcon_port,
            self.server.rcon_pass
        )

        self.discord = ServerBot(self.rcon, self.server)

        if should_restart:
            self.scheduler = AsyncIOScheduler()
            self.scheduler.add_job(
                self.daily_restart,
                trigger='cron',
                hour=restart_hour,
                minute=restart_minute
            )
            self.scheduler.start()
            print("Will restart server in off hours.")

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

    """TOP LEVEL FUNCTIONS"""

    async def daily_restart(self):
        """Restarts the server depending on population."""
        if not wait_for_pop:
            await self.restart_server_and_manager()
        if a2s_info((server_ip, self.server.query_port))['players'] >= restart_pop_threshold:
            await self.discord.func['debug_message'](f"Server still populated, delaying restart by {restart_pop_delay}")
            self.scheduler.add_job(
                self.daily_restart,
                trigger='cron',
                hour=restart_hour + int(restart_pop_delay / 60),
                minute=restart_minute + int(restart_pop_delay % 60)
            )
        else:
            await self.restart_server_and_manager()

    async def download_server(self, steamcmd, path, app_id):
        """Downloads the new version of the app to the specified folder. Returns stdout string or stderr string."""
        process = await asyncio.create_subprocess_shell(
            f'{steamcmd} +login anonymous +force_install_dir "{path}" +app_update {app_id} validate +quit',
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT
        )
        stdout, stderr = await process.communicate()
        if stderr is None:
            print(stdout.decode().strip())
        else:
            print(stderr.decode().strip())

    # I'm not confident that this feature will work quite yet.
    async def update_task(self):
        while not await self.listener.update_exists(403240):
            await asyncio.sleep(60)
        update_temp_path = f"{server_path}\\..\\_MANAGER_UPDATE"
        dl_result = await self.download_server(steamcmd, update_temp_path, server_appid)
        if dl_result.endswith(f"Success! App '{server_appid}' fully installed."):
            await self.discord.func['debug_message']('New server update downloaded, waiting for client to be updated.')
            # Wait for client to be pushed
            while not await self.listener.update_exists(client_appid):
                await asyncio.sleep(30)
            # Broadcast to server that new client is released
            self.rcon.send_command(f'adminbroadcast {update_broadcast_message}')
            self.rcon.send_command(f'adminbroadcast {restart_broadcast_message}')
            time.sleep(60)  # should this be blocking?
            # Kill the server process
            self.process.terminate()
            # Update file operations
            shutil.copyfile(f"{self.server.path}\\{self.server.start}", f"{update_temp_path}\\{self.server.start}")
            shutil.rmtree(f"{update_temp_path}\\Squad\\ServerConfig")
            shutil.copytree(f"{self.server.path}\\Squad\\ServerConfig", f"{update_temp_path}\\Squad\\ServerConfig")
            shutil.move(self.server.path, f"{self.server.path}\\..\\old-server-backup")
            shutil.move(f"{update_temp_path}", self.server.path)
            self.start_server_and_exit()
        else:
            await self.discord.func['debug_message']('Error! Something went wrong downloading the update.')
            await self.discord.func['debug_message']('steamcmd output:', dl_result)

    """HELPFUL SHIT"""

    async def close_discord_client(self):
        asyncio.ensure_future(self.discord.client.logout(), loop=self.loop)

    async def restart_server_and_manager(self):
        """Kills the server and manager, and restarts both."""
        await self.rcon.send_command(f'adminbroadcast {restart_broadcast_message}')
        time.sleep(restart_warn_time * 60)  # Should this be blocking?
        await self.close_discord_client()
        print("Terminating process...")
        self.process.terminate()
        print("Restarting server...")
        self.start_server_and_exit()

    def start_server_and_exit(self):
        # Magical directory adventure! Fix this.
        h = os.getcwd()
        os.chdir(self.server.path)
        os.system(f'cmd.exe /c {self.server.start}')
        os.chdir(h)
        # Brute force solution
        os.system(f'.\\venv\\Scripts\\activate.bat & python main.py')
        exit()

    async def is_server_running(self):
        """Poorly named or badly implemented"""
        if self.process.is_running():
            await asyncio.sleep(1)
            await self.is_server_running()
        else:
            print("Server process is not running! Has the server crashed?")  # send to discord bot instead.
            await self.restart_server()  # PLS FIX
