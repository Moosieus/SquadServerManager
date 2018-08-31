import datetime, shutil
from miscellaneous.misc import frmt_td
from squad_ftp.ftp import *
from server_config import local_path, ftp_path, server_ip


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


class SquadFileUtils:
    """Contains all of the information about a server_scripts's setup, and the functions to retrieve it."""
    def __init__(self):
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        print("SquadFileUtils")
        try:
            self.sq_ftp = SqFTP()
        except:
            print("FTP CONNECTION FAILED!")
            self.sq_ftp=False

    async def get_rcon_info(self):
        """Parses rcon.cfg for the ip, port, and password."""
        if type(self.sq_ftp) is not bool:
            if os.path.exists(f'{local_path}\\Rcon.cfg'):
                os.remove(f'{local_path}\\Rcon.cfg')
            print(f'{ftp_path}/Squad/ServerConfig/Rcon.cfg')
            await pull_file(self.sq_ftp.ftp, f'{ftp_path}/Squad/ServerConfig/Rcon.cfg', f'{local_path}\\Rcon.cfg')
        else:
            print("self.sq_ftp not initialized, cannot pull Rcon.cfg. Attempting to use local store...")
        rcon_cfg_dict = parse_cfg(f'{local_path}\\Rcon.cfg')
        if rcon_cfg_dict['IP'] == '0.0.0.0':
            rcon_cfg_dict['IP'] = server_ip
        rcon_cfg_dict['Port'] = rcon_cfg_dict['Port'].strip(' ')
        rcon_cfg_dict['Password'] = rcon_cfg_dict['Password'].strip(' ')
        return rcon_cfg_dict

    async def get_ban(self, steam_id64):
        """Checks to see if a user is banned. Returns a message string."""
        ftp_ban_path = f'{ftp_path}/Squad/ServerConfig/Bans.cfg'
        local_ban_path = f'{local_path}\\Bans.cfg'
        await pull_file(self.sq_ftp.ftp, ftp_ban_path, local_ban_path)
        try:
            with open(local_ban_path, 'r', encoding='utf-8') as ban_file:
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

    async def set_ban(self, steamid64, time_stamp=0, ds_comment='', remove=False):
        """Sets a ban in the bans.cfg file. Always written at the bottom of the file. Map change required."""
        local_ban_path = f'{local_path}\\Bans.cfg'
        ftp_ban_path = f'{ftp_path}/Squad/ServerConfig/Bans.cfg'
        temp_path = f'{local_path}\\Bans_tmp.cfg'
        await pull_file(self.sq_ftp.ftp, ftp_ban_path, local_ban_path)

        with open(local_ban_path, 'r', encoding='utf-8') as ban_file:
            with open(temp_path, 'w', encoding='utf-8') as tmp_file:
                comment = ''
                for line in ban_file:
                    if steamid64 not in line:
                        tmp_file.write(line)
                    else:
                        comment = line.split('//', 1)[1].rstrip('\n')
                if not remove:
                    tmp_file.write(f'\n{steamid64}:{time_stamp} //{comment} > {ds_comment}')
        backup_path = local_ban_path.replace('Bans.cfg', 'Bans_Backup.cfg')
        if os.path.exists(backup_path):
            os.remove(backup_path)
        shutil.copyfile(local_ban_path, backup_path)
        os.remove(local_ban_path)
        os.rename(temp_path, local_ban_path)
        if not compare_files(self.sq_ftp.ftp, ftp_ban_path, local_ban_path):
            await push_file(self.sq_ftp.ftp, ftp_ban_path, local_ban_path)
        else:
            await self.set_ban(steamid64, time_stamp=time_stamp, ds_comment=ds_comment, remove=remove)
