class Tile:
    def __init__(self):
        """Initialize an empty tile"""
        self.__isPit = False
        self.__numBreeze = 0
        self.__isWumpus = False
        self.__numStench = 0
        self.__isGold = False
        self.__isPlayer = False

    # Getters
    def getPit(self):
        return self.__isPit

    def getBreeze(self):
        return False if self.__numBreeze == 0 else True

    def getWumpus(self):
        return self.__isWumpus

    def getStench(self):
        return False if self.__numStench == 0 else True

    def getGold(self):
        return self.__isGold

    def getPlayer(self):
        return self.__isPlayer

    # Setters
    def setPit(self):
        self.__isPit = True

    def setBreeze(self):
        self.__numBreeze += 1

    def setWumpus(self):
        self.__isWumpus = True

    def setStench(self):
        self.__numStench += 1

    def setGold(self):
        self.__isGold = True

    def setPlayer(self):
        self.__isPlayer = True

    # Removers   
    def removeWumpus(self):
        self.__isWumpus = False

    def removeStench(self):
        self.__numStench -= 1

    def removeGold(self):
        self.__isGold = False

    def removePlayer(self):
        self.__isPlayer = False
