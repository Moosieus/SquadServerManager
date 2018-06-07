# Squad Server Manager
#### A program that manages your Squad server, performing numerous funtions.

### Installation Instructions:
1. Install Python 3.6
2. Download this repository and store it where you want it to be installed.
3. Open a command prompt, navigate to the installation folder, and run `pip install .` This will install the dependencies required
4. Fill in the necessary settings in `server_config.py`
5. Add your user id to the Admins.cfg file
6. With the squad server running, and server_cfg.py filled out, run `main.py`

### Usage:
Issue commands over the bot, or configure behaviors in `server_config.py`

### What the manager can currently do:
+ Automatically restart the server, while ensuring the server does not restart until the population has dropped below the specified threshold.
+ Automatically update the server when updates are available (EXPERIMENTAL)
+ Allow RCON access to the server over discord, with an easy to use interface (read `bot help.md` for details, or use ...help)
+ Edit and view bans from the server's Bans.cfg file, allowing users to retrieve bans, and to modify them.

### Things I hope to implement:
 + Make a better permissions system for discord
 + Log all interactions with the discord bot
 + Automatic restarts on server crashes
 + Auto install workshop content to a server
 + Automatic broadcasts on certain events
 + Enable voting for maps
 + Allow Discord bot to whitelist players
 + Enable users to easily add their own code and behaviors
 + Network monitoring via psutil
 + Track player count and hardware level network data
 + Warn about potential misconfiguration in server files
