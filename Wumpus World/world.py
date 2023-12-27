from tile import *
import numpy as np

class WumpusWorld:
    def __init__(self):
        """Initialize an empty board"""
        self.height = 0
        self.width = 0
        self.numGold = 0
        self.numWumpus = 0
        self.map = []
        self.matrix = []
        self.doorPos = None

    def getAdjacents(self, i, j):
        adj = []
        if i - 1 >= 0:
            adj.append((i - 1, j))
        if i + 1 <= self.height - 1:
            adj.append((i + 1, j))
        if j - 1 >= 0:
            adj.append((i, j - 1))
        if j + 1 <= self.width - 1:
            adj.append((i, j + 1))
        return adj
    
    def readMap(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
                self.height = len(lines)
                tiles = []
                for line in lines:
                    tiles.append(line.split('.'))
                self.width = len(tiles[0])

                # Empty tiles map
                for i in range(self.height):
                    row = []
                    for j in range(self.width):
                        row.append(Tile())
                    self.map.append(row)

                # Tile's objects
                for i in range(self.height):
                    for j in range(self.width):
                        if 'G' in tiles[i][j]:
                            (self.map[i][j]).setGold()
                            self.numGold += 1
                        if 'P' in tiles[i][j]:
                            (self.map[i][j]).setPit()
                            adj = self.getAdjacents(i, j)
                            for a in adj:
                                (self.map[a[0]][a[1]]).setBreeze()
                        if 'W' in tiles[i][j]:
                            (self.map[i][j]).setWumpus()    
                            adj = self.getAdjacents(i, j)
                            self.numWumpus += 1
                            for a in adj:
                                (self.map[a[0]][a[1]]).setStench()
                        if 'A' in tiles[i][j]:
                            (self.map[i][j]).setPlayer()
                            self.doorPos = (i, j)
                #
        except IOError:
            return None
        with open(filename, 'r') as f:
            temp = []
            lines = f.read().splitlines()
            for line in lines:
                temp.append(line.split('.'))
        temp = np.array(temp)
        self.matrix = temp

    def generateMap(self, numPit, numWumpus, numGold):
        pass

    def grabGold(self, i , j):
        self.numGold -= 1
        self.map[i][j].removeGold()

    def killWumpus(self, i, j):
        self.numWumpus -= 1
        self.map[i][j].removeWumpus()
        adj = self.getAdjacents(i, j)
        for a in adj:
            if self.map[a[0]][a[1]].getStench():
                self.map[a[0]][a[1]].removeStench()

    def movePlayer(self, before_i, before_j, after_i, after_j):
        self.map[before_i][before_j].removePlayer()
        self.map[after_i][after_j].setPlayer()

    def leftGold(self):
        return False if self.numGold == 0 else True

    def leftWumpus(self):
        return False if self.numWumpus == 0 else True