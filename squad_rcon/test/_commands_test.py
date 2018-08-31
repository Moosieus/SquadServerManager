import re
from squad_rcon.commands import commands

tests = []
cases = {
    'kick': (
        ('AdminKick moose teamkilling loser', True),
        ('AdminKick 0 gigantafag', True)
    ),
    'kickid': (
        ('AdminKickById 0 Normies get out REEEEEE', True),
        ('AdminKickById 76 ( ͡° ͜ʖ ͡°)', True)
    ),
    'ban': (
        ('AdminBan pernis 3M No men allowed', True),
        ('AdminBan 13 0 13 is an unlucky number.', True)
    ),
    'banid': (
        ('AdminBanById 13 0 took my bradley >:C', True),
        ('AdminBanById 13 1M WCT has badmins', True),
        ('AdminBanById notanID wooloolooo loo', False)
    ),
    'broadcast': (
        ('AdminBroadcast This is a test broadcast', True),
        ('AdminBroadcast 0', True),
        ('AdminBroadcast <=>', True)
    )
}

def test_command(key):
    for test in cases[key]:
        if re.match(commands[key], test[0]) is None:
            print(test[0], f'Passed = {test[1] is False}')
        else:
            print(test[0], f'Passed = {test[1] is True}')

for key in cases:
    test_command(key)
