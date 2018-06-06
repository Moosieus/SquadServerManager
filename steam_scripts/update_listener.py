from steam import client
from server_config import server_appid, client_appid

class UpdateListener:
    """Checks for whether or not a game branch has an update."""
    def __init__(self, server_build_time, client_build_time, app_id=403240):
        self.cli = client.SteamClient()
        self.app_id = app_id
        self.current_update = {
            server_appid: server_build_time,
            client_appid: client_build_time
        }

    async def get_last_update(self, app_id):
        """Returns the unix time of the last update on the public branch of the Squad Dedicated Server."""
        if self.cli.connected is False:
            self.cli.anonymous_login()
        return self.cli.get_product_info(apps=[app_id]) \
            ['apps'] \
            [app_id] \
            ['depots'] \
            ['branches'] \
            ['public'] \
            ['timeupdated']

    async def update_exists(self, app_id):
        """Returns true when an update exists, else runs again"""
        if int(await self.get_last_update(app_id)) > int(self.current_update[app_id]):
            return True
        else:
            return False
