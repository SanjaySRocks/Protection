**This Project was created to Protect Gameserver from DDoS attacks using firewall.**

##### Q. HOW DOES IT PROTECT GAMESERVER?
A. iplogger.amxx logs ips of currently playing players inside server and use those ips in firewall, which will allow traffics only to those online players and blocks all other traffic completly.


##### INSTALLATION & USAGE:-
1. Put `iplogger.amxx` -> /addons/amxmodx/plugins/
2. Put `ddos.sh` -> /root/ directory
3. To make file executable use `chmod +x ddos.sh`
4. Edit `ddos.sh` and Update your iplog file path
5. Install screen or nohup whatever you like and run `ddos.sh` script in background
