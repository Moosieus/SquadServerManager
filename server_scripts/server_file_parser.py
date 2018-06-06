import os, re, datetime, shutil
from miscellaneous.misc import frmt_td
from server_config import server_appid, client_appid

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


class SquadServer:
    """Contains all of the information about a server_scripts's setup, and the functions to retrieve it."""
    def __init__(self, folder_path, start_file, ip, name=None):
        if not os.path.isdir(folder_path):
            raise FileNotFoundError
        elif not os.path.isfile(f'{folder_path}\\{start_file}'):
            raise FileNotFoundError

        self.path = folder_path
        self.ip = ip
        self.start = start_file
        self.name = name
        self.parse_start_file() # game_port, query_port
        self.parse_server_cfg() # name, cfg_max_players, cfg_reserves, cfg_password, cfg_vic_claim
        self.parse_rcon_cfg() # rcon_ip, rcon_port, rcon_pass

    def parse_start_file(self):
        """Parses start script for the game port and query port."""
        with open(f'{self.path}\\{self.start}', 'r', encoding='utf-8') as start_file:
            start_content = start_file.read().lower()
            self.game_port = int(
                re.search(r'port=\d+', start_content)[0]
                    .split('=', 1)[1]
            )
            self.query_port = int(
                re.search(r'queryport=\d+', start_content)[0]
                    .split('=', 1)[1]
            )

    def get_server_build_time(self):
        """Saves the server_scripts's build id and returns it. Server must be up to date on first run."""
        build_path = f'{self.path}\\server_build_id.txt'
        if os.path.isfile(build_path):
            return int(open(build_path, 'r').read())

        else:
            with open(build_path, 'w') as build_txt:
                print("YOUR SERVER MUST BE UP TO DATE FOR THE FIRST TIME SETUP!") # I'm so good at this
                num = input(f'Copy / Paste the "timeupdated" of the public branch here: https://steamdb.info/app/{server_appid}/depots/?branch=public\n')
                num = re.search('\d+', num)[0]
                build_txt.write(num)
                return num

    def get_client_build_time(self):
        """Saves the server_scripts's build id and returns it. Server must be up to date on first run."""
        build_path = f'{self.path}\\client_build_id.txt'
        if os.path.isfile(build_path):
            return int(open(build_path, 'r').read())

        else:
            with open(build_path, 'w') as build_txt:
                print("YOUR SERVER MUST BE UP TO DATE FOR THE FIRST TIME SETUP!") # I love copying mistakes
                num = input(f'Copy / Paste the "timeupdated" of the public branch here: https://steamdb.info/app/{client_appid}/depots/?branch=public\n')
                num = re.search('\d+', num)[0]
                build_txt.write(num)
                return num

    def parse_rcon_cfg(self):
        """Parses rcon.cfg for the ip, port, and password."""
        rcon_cfg_dict = parse_cfg(f'{self.path}\\Squad\\ServerConfig\\Rcon.cfg')
        if rcon_cfg_dict['IP'] == '0.0.0.0':
            self.rcon_ip = '100.36.106.14' # input("please enter the server_scripts's public IP:")
        else:
            self.rcon_ip = rcon_cfg_dict['IP']
        self.rcon_port = rcon_cfg_dict['Port'].strip(' ')
        self.rcon_pass = rcon_cfg_dict['Password'].strip(' ')

    def parse_server_cfg(self):
        """Parses Server.cfg for the default player cap, reserve slots, password, and claim state."""
        server_cfg_dict = parse_cfg(f'{self.path}\\Squad\\ServerConfig\\Server.cfg')
        if self.name is None:
            self.name = server_cfg_dict['ServerName'].strip('"')
        self.cfg_max_players = int(server_cfg_dict['MaxPlayers'])
        self.cfg_reserves = int(server_cfg_dict['NumReservedSlots'])
        self.cfg_password = server_cfg_dict['ServerPassword'].lower() # Server passwords do not use capital letters.
        self.cfg_vic_claim = bool(server_cfg_dict['VehicleClaimingDisabled'])


    """BANS"""

    def is_banned(self, steam_id64):
        """Checks to see if a user is banned. Returns a message string."""
        try:
            with open(f'{self.path}\\Squad\\ServerConfig\\Bans.cfg', 'r', encoding='utf-8') as ban_file:
                for line in ban_file:
                    if steam_id64 in line:
                        try:
                            ban_string = f'{steam_id64} was banned, '
                            time_stamp = int(line.split(':', 1)[1].split(' ', 1)[0])
                            if time_stamp is 0:
                                ban_string += 'forever.'
                            else:
                                date = datetime.datetime.fromtimestamp(time_stamp)
                                ban_string += 'until ' + date.strftime('%Y-%m-%d %H:%M') + ', '
                                time_until = date - datetime.datetime.now()
                                ban_string += f'{frmt_td(time_until)}.'
                            reason = line.split('//', 1)[1].strip('\n')
                        except:
                            return f'Error: SteamID was found in bans.cfg, but the line was invalid.'
                        return f'{ban_string}\nMessage: {reason}'
                return 'Steam ID was not found in bans.cfg. User is not banned locally.'
        except:
            return 'Error: Failed to open and read Bans.cfg.'

    def set_ban(self, steamid64, time_stamp=0, ds_comment='', remove=False):
        ban_path = f'{self.path}\\Squad\\ServerConfig\\Bans.cfg'
        tmp_path = f'{self.path}\\Squad\\ServerConfig\\bans_tmp.cfg'
        """Sets a ban in the bans.cfg file. Always written at the bottom of the file. Map change required."""
        with open(ban_path, 'r', encoding='utf-8') as ban_file:
            with open(tmp_path, 'w', encoding='utf-8') as tmp_file:
                comment = ''
                for line in ban_file:
                    if steamid64 not in line:
                        tmp_file.write(line)
                    else:
                        comment = line.split('//', 1)[1].rstrip('\n')
                if not remove:
                    tmp_file.write(f'\n{steamid64}:{time_stamp} //{comment} > {ds_comment}')
        # Replace and rename the files.
        backup_path = ban_path.replace('\\ServerConfig', '\\ServerConfig\\banbackup')
        if os.path.exists(backup_path[:-8]):
            shutil.rmtree(backup_path[:-8])
            os.mkdir(backup_path[:-8])
        else:
            os.mkdir(backup_path[:-8])
        os.rename(ban_path, backup_path)
        os.rename(tmp_path, ban_path)
