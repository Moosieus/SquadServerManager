from server_config import ftp_ip, ftp_port, ftp_passwd, ftp_user, ftp_path
import paramiko
import asyncio, os


def compare_files(ftp: paramiko.SFTPClient, ftp_path: str, local_path: str):
    """Returns True if remote file is newer, else False."""
    if not os.path.exists(local_path):
        return True
    ftp_path = ftp_path.replace('\\', '/')
    file_date = round(os.path.getmtime(local_path), 0)
    ftp_date = ftp.stat(f'{ftp_path}').st_mtime
    if ftp_date > file_date: # Be careful there's no time delta
        return True
    return False


async def pull_file(ftp: paramiko.SFTPClient, ftp_path: str, local_path: str):
    """Pulls file from remote path to local path only if out of date."""
    if compare_files(ftp, ftp_path, local_path):
        ftp.get(ftp_path, local_path)
    else:
        print("Local is up to date.")


async def push_file(ftp: paramiko.SFTPClient, ftp_path: str, local_path: str):
    """Pushes file to remote if local is more up to date, else raises error."""
    if not compare_files(ftp, ftp_path, local_path):
        print(f'Pushing {local_path} to {ftp_path}')
        ftp.put(local_path, ftp_path)
    else:
        raise Exception("Error! FTP file was updated.")


class SqFTP:

    def __init__(self):
        # Create FTP client and login
        self.transport = paramiko.Transport((ftp_ip, ftp_port))
        self.transport.connect(username=ftp_user, password=ftp_passwd)
        self.ftp = paramiko.SFTPClient.from_transport(self.transport)
        # Navigate to the relevant directories
        self.ftp.chdir(f'{ftp_path}/Squad/ServerConfig')
        print(self.ftp.getcwd())
        # Download the initial files

    async def keep_alive(self, interval=60):
        # print('Keeping connection alive')
        """Sends a command on an interval to keep the connection alive."""
        self.ftp.getcwd()
        await asyncio.sleep(interval)
        await self.keep_alive()
