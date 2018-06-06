"""
A dictionary of all the commands Squad RCON supports.
Each command is matched to a regular expression.
"""

commands = {
    'kick': r'AdminKick (\d{1,2}|.*).*',
    'kickid': r'AdminKickById \d{1,2}.*',
    'ban': r'AdminBan (\d{1,2}|.*) (0|\d+[\w\D]).*',
    'banid': r'AdminBanById \d{1,2} (0|\d+[\w\D]).*',
    'broadcast': r'AdminBroadcast .*',
    'restartmatch': r'AdminRestartMatch',
    'endmatch': r'AdminEndMatch',
    'killserver': r'AdminKillServer',
    'changemap': r'AdminChangeMap [\w\s\d]+',
    'setnextmap': r'AdminSetNextMap [\w\s\d]+',
    'setmaxplayers': r'AdminSetMaxNumPlayers \d{1,2}',
    'setreservedslots': r'AdminSetNumReservedSlots \d{1,2}',
    'setpassword': r'AdminSetServerPassword .*',
    'slomo': r'AdminSlomo (\d{1,100}.\d{1,100}|\d{1,100})',
    'teamchange': r'AdminForceTeamChange (.*|\d{1,2})',
    'teamchangeid': r'AdminForeTeamChangeById \d{1,2}',
    'validplacement': r'AdminAlwaysValidPlacement (0|1)',
    'vehicleclaiming': r'AdminDisableVehicleClaiming (0|1)',
    'setkitsavailable': r'AdminAllKitsAvailable (0|1)',
    'listdisconnected': r'AdminListDisconnectedPlayers',
    'listplayers': r'ListPlayers',
    'shownextmap': r'ShowNextMap',
}
