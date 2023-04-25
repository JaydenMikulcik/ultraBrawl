from Characters.playerDefault import Player
from Characters.blazeFist import blazeFist
from Characters.bloodMoon import bloodMoon
from Characters.deathBringer import deathBringer
from Characters.quantumKnight import quantumKnight





# All this function does is instantiate the correct player
def createPlayer(playerName, xposition, yposition, platforms):


    # Return blazeFist
    if playerName == "blazeFist":
        return blazeFist(xposition, yposition, platforms)
    

    # Return bloodMoon
    elif playerName == "bloodMoon":
        return bloodMoon(xposition, yposition, platforms)
    

    # Return deathBringer
    elif playerName == "deathBringer":
        return deathBringer(xposition, yposition, platforms)
    

    # Return quantumKnight
    elif playerName == "quantumKnight":
        return quantumKnight(xposition, yposition, platforms)
    

    # Return the player default
    else:
        return Player(xposition, yposition, platforms)

