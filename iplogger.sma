#include <amxmodx>

#if AMXX_VERSION_NUM > 183
#define client_disconnect client_disconnected
#endif

#define MAX_PLAYERS        32
#define MAX_PLAYER_IP_SIZE 16 // Without port.

new const g_szFileName[] = "current_players_ips.log"
new g_szCurrentPlayersIPFilePath[128]

public plugin_init() {
	register_plugin("Current Players IP Logger", "1.3-beta", "AMX Mod Dev")

	formatex(g_szCurrentPlayersIPFilePath, charsmax(g_szCurrentPlayersIPFilePath), "addons/amxmodx/logs/%s", g_szFileName)

	if(file_exists(g_szCurrentPlayersIPFilePath)) {
		delete_file(g_szCurrentPlayersIPFilePath)
	}
}

public client_putinserver(iPlayerID) { // Use "PutInServer" because "ClientDisconnect" will not be called when the player disconnect before.
	#if !defined USE_HLTV_N_BOT_LOGGING
	if(is_user_hltv(iPlayerID) || is_user_bot(iPlayerID))
		return
	#endif

	new szPlayerIPAddress[16]

	if(get_user_ip(iPlayerID, szPlayerIPAddress, charsmax(szPlayerIPAddress), 1)) {
		new szIPsData[MAX_PLAYERS * MAX_PLAYER_IP_SIZE], iLength

		if(!file_exists(g_szCurrentPlayersIPFilePath)
		|| !read_file(g_szCurrentPlayersIPFilePath, 0, szIPsData, charsmax(szIPsData), iLength)
		|| iLength <= 0) {
			copy(szIPsData, charsmax(szIPsData), szPlayerIPAddress)
		}
		else if(contain(szIPsData, szPlayerIPAddress) != -1) {
			return
		}
		else {
			format(szIPsData, charsmax(szIPsData), "%s,%s", szIPsData, szPlayerIPAddress)
		}

		write_file(g_szCurrentPlayersIPFilePath, szIPsData, 0)
	}
}

public client_disconnect(iPlayerID) {
	#if !defined USE_HLTV_N_BOT_LOGGING
	if(is_user_hltv(iPlayerID) || is_user_bot(iPlayerID))
		return
	#endif

	if(!file_exists(g_szCurrentPlayersIPFilePath))
		return

	new szPlayerIPAddressData[3][18]
	get_user_ip(iPlayerID, szPlayerIPAddressData[0], charsmax(szPlayerIPAddressData[]), 1)
	formatex(szPlayerIPAddressData[1], charsmax(szPlayerIPAddressData[]), ",%s", szPlayerIPAddressData[0])
	formatex(szPlayerIPAddressData[2], charsmax(szPlayerIPAddressData[]), "%s,", szPlayerIPAddressData[0])

	new szIPsData[MAX_PLAYERS * MAX_PLAYER_IP_SIZE], iLength

	read_file(g_szCurrentPlayersIPFilePath, 0, szIPsData, charsmax(szIPsData), iLength)

	if(replace(szIPsData, charsmax(szIPsData), szPlayerIPAddressData[1], "")
	|| replace(szIPsData, charsmax(szIPsData), szPlayerIPAddressData[2], "")
	|| replace(szIPsData, charsmax(szIPsData), szPlayerIPAddressData[0], "")) {
		write_file(g_szCurrentPlayersIPFilePath, szIPsData, 0)
	}
}
