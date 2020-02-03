import subprocess
import psutil
import time
import sys
import getopt
import echovr_api

def findProcess():
    for process in psutil.process_iter():
        if process.name() == "echovr.exe":
            return True
    return False

def getId(old):
    try:
        gameState = echovr_api.fetch_state()
        tempMatch = gameState.sessionid
        if (tempMatch != old):
            print("found a new match with id: " + tempMatch)
            return tempMatch
        else:
            return old
    except:
        return old
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
    while True:
        if(findProcess()):
            matchId = getId(matchId)
        else:
            print("Game Closed!")
            if matchId:
                print("recovering to match: " + matchId)
                command = "\"" + path + "\""  + " -lobbyid " + matchId
                subprocess.Popen(command)
            else:
                print("No Match ID Stored")
        time.sleep(2)
