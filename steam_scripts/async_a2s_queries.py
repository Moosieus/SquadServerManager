"""
Steam yeilds the information we need over a2s, but reports higher player count than actually in game / has blank names.
It'll work for now I guess
Is this stuff even necessary? Probably not.
"""

from steam.game_servers import a2s_info, a2s_players, a2s_rules


async def get_server_info(ip, query_port):
    return a2s_info((ip, query_port))


async def get_server_players(ip, query_port):
    return a2s_players((ip, query_port))


async def get_server_rules(ip, query_port):
    return a2s_rules((ip, query_port))
