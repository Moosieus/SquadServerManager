from server_scripts.server_manager import ServerManager
from server_scripts.server_file_parser import SquadServer
from server_config import server_path, start_file, server_ip, server_name

"""Run this file from a command prompt to start the manager."""

my_server = SquadServer(
    server_path,
    start_file,
    server_ip,
    name=server_name
)

x = ServerManager(my_server)
