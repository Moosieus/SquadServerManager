## Rcon Commands:
+ help - Shows this dialogue.
+ kick {name or id} {reason} - kicks a player from the server
+ kickid {id} {reason} - kick only using ids
+ ban {name or id} {time} {reason} - bans a player from the server
+ banid {id} {time} {reason} - ban only using ids
+ broadcast {message} - Broadcasts a message at the top of each players screen
+ restartmatch - Resets the current match
+ endmatch - Ends the current match
+ killserver - stops the server - DANGEROUS!
+ changemap {map} - Instantly ends the match and changes to specified map
+ setnextmap {map} - Sets the next map in the rotation
+ setmaxplayers {num} - Sets the maximum number of players allowed on the server
+ setreservedslots {num} - Sets the number of reserved slots on the server
+ setpassword {password} - Sets a password on the server
+ slomo {multi} - Sets the game speed to 1 x multi. - DANGEROUS
+ teamchange {name or id} - Changes what team a player is on
+ teamchangeid {id} - Teamchange only using ids
+ validplacement {0 or 1} - Allows deployables to be placed anywhere
+ vehicleclaiming {0 or 1} - Allows vehicles to be claimed without SL approval
+ setkitsavailable {0 or 1} - Allows players to use all kits
+ listdisconnected - Lists the recently disconnected players
+ listplayers - Lists the current players on the server
+ shownextmap - Shows the next map
## Server Commands
+ getban {steamid64} - Searches the Bans.cfg file for the banned user
+ setban {steamid64} {1M, 3W, 7D, 24H, or remove} - Edits or adds a ban in the Bans.cfg file
## Bot commands
+ MakeAdmin {User ID} {Comment} - Allows a user to interact with the bot.
+ RemoveAdmin {User ID} - Disallows a user to use the discord bot.
+ RefreshAdmins - Refreshes the admin list from the bots admin file.
