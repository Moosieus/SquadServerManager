import re, asyncio
from aiorcon.rcon import RCON
from fuzzywuzzy import fuzz
from squad_rcon.commands import commands

def doNothing(*args):
    return False

class SquadRconClient:
    """Simple command checks to ensure rcon is not passed invalid commands."""
    def __init__(self, ip, port, password, timeout=5):
        loop = asyncio.get_event_loop()
        print("Starting rcon...")
        loop.run_until_complete(self.setup_rcon(ip, port, password, timeout=timeout))
        print("Rcon connected!")
        loop.run_until_complete(self.rcon('ListPlayers'))

    async def setup_rcon(self, ip, port, password, timeout=5):
        """RCON setup must be asynchronous, cannot be ran in __init__."""
        self.rcon = await RCON.create(
            ip,
            port,
            password,
            loop=asyncio.get_event_loop(),
            multiple_packet=False,
            timeout=timeout,
            auto_reconnect_cb=doNothing # I have no idea what this does
        )

    async def send_command(self, request):
        """Execute a command on squad_rcon, using simple interpretation."""
        request_list = re.split(r'[\W]', request.lower())

        best_match = ("", 0)
        for command in commands:
            match_value = fuzz.partial_ratio(command, request_list[0])
            if match_value > best_match[1]:
                best_match = (command, match_value)
        if best_match[1] < 50:
            raise Exception('No strong matching commands.')
        revised_request = commands[best_match[0]].split(' ', 1)[0] + request[len(request_list[0]):]

        match = re.match(commands[best_match[0]], revised_request)
        if match is None:
            return 'Command parameters failed to match.'
        try:
            return await self.rcon(revised_request)
        except TypeError:
            return 'Command was sent but yielded no return. Command may or may not have worked.'

    async def direct_command(self, request):
        """Execute a squad_rcon command, ensuring the command exists."""
        if request.split(' ', 1)[0] in [s.split(' ', 1)[0] for s in commands.values()]:
            return await self.rcon(request)
        raise Exception('No match found.')
