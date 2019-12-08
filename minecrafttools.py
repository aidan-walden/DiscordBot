import time
import json
import asyncio
from datetime import datetime

class MinecraftPlayer:
    uuid = ""
    username = ""
    playerOnServer = False
    playerLoginTime = playerLogoutTime = None

    def __init__(self, username, uuid):
        self.username = username
        self.uuid = uuid

        playerExists = False
        with open('mcPlayers.json', 'r') as json_file:
            data = None
            try:
                data = json.load(json_file)
                for p in data['minecraftUsers']:
                    if p['uuid'] == uuid:
                        playerExists = True
                if not playerExists:
                    data['minecraftUsers'] = []
                    data['minecraftUsers'].append({
                        'username': username,
                        'uuid': uuid,
                        'longestSes': '00:00'
                    })

            except json.decoder.JSONDecodeError:
                data = {}
                data['minecraftUsers'] = []
                data['minecraftUsers'].append({
                    'username': username,
                    'uuid': uuid,
                    'longestSes': '00:00'
                })

            with open('mcPlayers.json', 'w') as outfile: #Save
                json.dump(data, outfile)
    def isPlayerOnServer(self, playerList, uuid):
        '''Checks given player list for the given UUID.'''
        for player in playerList:
            playerUuid = player.split('(')[1][:-2]
            if(playerUuid == uuid):
                return True
        return False

    def playerConnectionChange(self, connected):
        '''
        Called when a player has changed their connection to the Minecraft server, to determine whether they logged in or out.
        Will also shelve their session time if it is greater than the longest one already shelved.
        '''
        if connected and not self.playerOnServer:
            print(self.username + ' LOGGED IN')
            self.playerOnServer = True
            self.playerLoginTime = datetime.now()
        elif self.playerOnServer:
            print(self.username + ' LOGGED OUT')
            self.playerOnServer = False
            self.playerLogoutTime = datetime.now()
            playerSessionTime = self.playerLogoutTime - self.playerLoginTime
            sec = playerSessionTime.seconds
            hours = sec // 3600
            minutes = (sec // 60) - (hours * 60)
            finalTime = str(hours) + ':' + str(minutes)
            with open('mcPlayers.json') as json_file:
                data = json.load(json_file)
                recordHours = None
                for p in data['minecraftUsers']:
                    if(p['uuid'] == self.uuid):
                        recordHours = p['longestSes']
                        if recordHours == '00:00':
                            with open('mcPlayers.json', 'w') as newJson:
                                p['longestSes'] = finalTime
                                newJson.seek(0)
                                json.dump(data, newJson, indent=4)
                                newJson.truncate()
                        else:
                            if datetime.strptime(finalTime,'%H:%M') > datetime.strptime(recordHours,'%H:%M'):
                                p['longestSes'] = finalTime

    def trackPlayerHours(self, serverIp):
        '''Checks player list of given server IP for the player.'''
        import subprocess
        while(True):
            result = subprocess.Popen(['mcstatus', serverIp, 'status'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout,stderr = result.communicate()
            if 'Traceback' in stdout.decode(): #Expect mcstatus to fail about every other time you run it
                print('mcstatus crashed 1sec')
                time.sleep(15)
                continue
            if not 'No players online' in stdout.decode():
                output = stdout.decode().split('[')[1]
                output = output[:-3]
                players = output.split(',')
                if not self.playerOnServer:
                    if self.isPlayerOnServer(players,self.uuid):
                        self.playerConnectionChange(True)
                else:
                    if not self.isPlayerOnServer(players, self.uuid):
                        self.playerConnectionChange(False)
            else:
                self.playerConnectionChange(False)
            time.sleep(15)

async def getServerInfo(serverIp):
    '''Returns basic info about a Minecraft server at the given IP.'''
    from mcstatus import MinecraftServer

    server = MinecraftServer.lookup(serverIp)
    try:
        status = server.status()
    except:
        return "That server is either offline or has an invalid IP address."
    return f"Ping: {status.latency} Players online: {status.players.online}"

async def getServerPlayers(serverIp):
    '''Returns the names of players on a Minecraft server at the given IP.'''
    from mcstatus import MinecraftServer

    server = MinecraftServer.lookup(serverIp)
    query = server.query()

    return query.players.names
