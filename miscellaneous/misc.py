"""A bunch of helpful functions that don't really fit into any one class, but are helpful."""
import re, datetime


def str_to_epoch(length_string):
    """Takes a number and letter, and returns a length in integer seconds."""
    length_string = length_string.lower()
    multi_dict = {
        'y': int(3.154e+7),
        'm': int(2.592e+6),
        'w': 604800,
        'd': 86400,
        'h': 60
    }
    number = re.match(r'\d+', length_string)
    multi = length_string[-1]
    return multi_dict[multi] * int(number[0])


def epoch_from_now(length):
    """Adds 'length' seconds to the current unix timestamp."""
    return round(datetime.datetime.now().timestamp()) + length


def frmt_td(time_delta):
    """Formats a datetime.timedelta into a 'time remaining' string."""
    t = {}
    seconds = round(time_delta.total_seconds())
    if seconds < 0:
        return 'date has been passed'
    t['months'], seconds = divmod(seconds, 2.628e+6)
    t['days'], seconds = divmod(seconds, 86400)
    t['hours'], seconds = divmod(seconds, 3600)
    t['minutes'], seconds = divmod(seconds, 60)
    t_string = ''
    for k,v in t.items():
        if v != 0:
            t_string += f'{int(v)} {k}, '
    return t_string[:-2]


def is_steamid64(steamid64):
    """Basic check to see if the given ID is likely a steam ID  (not perfect)."""
    try:
        int(steamid64)
        if len(steamid64) != 17:
            return False
        return True
    except ValueError:
        return False
