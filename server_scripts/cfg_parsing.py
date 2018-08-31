import os, datetime
from miscellaneous.misc import frmt_td
from server_config import server_ip # server ip as a string, '144.217.11.233'


def parse_cfg(path, encoding='utf-8'):
    """Returns all parameters in a cfg file as a dictionary."""
    cfg_dict = {}
    try:
        with open(path, 'r', encoding=encoding) as cfg:
            for line in cfg:
                line = line.strip('\n')
                if '//' in line:
                    line = line.split('//', 1)
                    line = line[0].strip(' ')
                if '=' in line and len(line) > 0:
                    line = line.split('=', 1)
                    line = [l.strip(' ') for l in line]
                    cfg_dict[line[0]] = line[1]
        return cfg_dict
    except FileNotFoundError:
        raise Exception(f"cfg file was not found: {os.path.basename(path)}")


def parse_rcon_cfg(file_path):
    """Returns all parameters in a cfg file as a dictionary."""
    cfg_dict = parse_cfg(file_path)
    if cfg_dict['IP'] == '0.0.0.0':
        print('rcon IP not specified, using server IP')
        ip = server_ip
    else:
        ip = cfg_dict['IP']
    port = int(cfg_dict['Port'].strip(' '))
    passwd = cfg_dict['Password'].strip(' ')
    return ip, port, passwd


def set_ban(file_path, steamid64, time_stamp=0, comment='', remove=False):
    """Sets a ban in the bans.cfg file. If entry exists, is moved to the bottom of the file."""
    temp_path = file_path + '.tmp'
    with open(file_path, 'r', encoding='utf-8') as ban_file:
        with open(temp_path, 'w', encoding='utf-8') as tmp_file:
            old_comment = ''
            for line in ban_file:
                if str(steamid64) not in line:
                    tmp_file.write(line)
                else:
                    old_comment = line.split('//', 1)[1].strip('\n')
            if not remove:
                if old_comment is '':
                    tmp_file.write(f'\n{steamid64}:{time_stamp} // {comment}')
                else:
                    tmp_file.write(f'\n{steamid64}:{time_stamp} //{old_comment} // {comment}')
    if os.path.exists(file_path + '.backup'):
        os.remove(file_path + '.backup')
    os.rename(file_path, file_path + '.backup')
    os.rename(temp_path, file_path)


def find_ban(file_path, steamid64):
    """Finds a ban in the specified ban file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as ban_file:
            for line in ban_file:
                if steamid64 in line:
                    try:
                        ban_string = f'{steamid64} was banned, '
                        time_stamp = int(line.split(':', 1)[1].split(' ', 1)[0])
                        if time_stamp is 0:
                            ban_string += 'forever.'
                        else:
                            date = datetime.datetime.fromtimestamp(time_stamp)
                            ban_string += 'until ' + date.strftime('%Y-%m-%c %H:%M') + ', '
                            time_until = date - datetime.datetime.now()
                            ban_string += f'{frmt_td(time_until)}.'
                        reason = line.split('//', 1)[1].strip('\n')
                    except:
                        return f'Error: SteamID was found in bans.cfg, but the line was invalid.'
                    return f'{ban_string}\nMessage: {reason}'
            return 'Steam ID was not found in bans.cfg. User is not banned locally.'
    except:
        return 'Error: Failed to open and read Bans.cfg.'
