import subprocess
import psutil
import time
import sys
import getopt
import requests

def fetch_state():
    req = requests.get("http://127.0.0.1:6721/session")
    return req.json()

def findProcess():
    for process in psutil.process_iter():
        if process.name() == "echovr.exe":
            return True
    return False

def getTeam(state):
    for player in state["teams"][0]["players"]:
        if player["name"] == state["client_name"]:
            return 0
    for player in state["teams"][1]["players"]:
        if player["name"] == state["client_name"]:
            return 1
    return 2

def getId(old,oldTeam):
    try:
        gameState = fetch_state()
        team = getTeam(gameState)
        tempMatch = gameState["sessionid"]
        if (tempMatch != old):
            print("found a new match with id: " + tempMatch)
            return (tempMatch,team)
        else:
            return (old,team)
    except:
        return (old,oldTeam)

if __name__ == "__main__":
    try:
        file = open("echopath.txt", 'r')
        path = file.read()
        file.close()
    except:
        file = open("echopath.txt", 'w')
        path = "C:\\Program Files\\Oculus\\Software\\Software\\ready-at-dawn-echo-arena\\bin\\win7\\echovr.exe"
        file.write(path)
        file.close()
    print("\nThis is the current path: \n\n\t" + path)
    print("\nIf your game is not stored in the default location, edit \"echopath.txt\" to contain the path to your game")
    time.sleep(5)
    matchId = ""
    team = 2
    
    while True:
        if(findProcess()):
            matchTuple = getId(matchId,team)
            matchId = matchTuple[0]
            team = matchTuple[1]
        else:
            print("Game Closed!")
            if matchId:
                print("recovering to match: " + matchId)
                if team == 0:
                    print("Joining Blue")
                elif team == 1:
                    print("Joining Orange")
                elif team == 2:
                    print("Joining Spectator")
                command = "\"" + path + "\""  + " -lobbyid " + matchId + " -lobbyteam " + str(team)
                subprocess.Popen(command)
            else:
                print("No Match ID Stored")
        time.sleep(2)
