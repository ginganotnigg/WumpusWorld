from tile import *
import numpy as np
import random as rd

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
        tiles = []
        try:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
                self.height = len(lines)
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
        self.matrix = np.array(tiles)

    def generateMap(self, numPit, numWumpus, numGold):
        self.width = self.height = 10
        for i in range(10):
            row = []
            for j in range(10):
                row.append(Tile())
            self.map.append(row)

        pos_x = rd.randint(0, 9)
        pos_y = rd.randint(0, 9)
        self.doorPos = (pos_x, pos_y)
        self.map[pos_x][pos_y].setPlayer()
        agentAdj = self.getAdjacents(self.doorPos[0], self.doorPos[1])

        # Add pit            
        for i in range(numPit):
            randPos = (rd.randint(0, 9), rd.randint(0, 9))
            while randPos == self.doorPos or randPos in agentAdj or self.map[randPos[0]][randPos[1]].getPit():
                randPos = (rd.randint(0, 9), rd.randint(0, 9))
            self.map[randPos[0]][randPos[1]].setPit()
            adj = self.getAdjacents(randPos[0], randPos[1])
            for a in adj:
                (self.map[a[0]][a[1]]).setBreeze()

        # Add gold
        self.numGold = numGold
        for i in range(self.numGold):
            randPos = (rd.randint(0, 9), rd.randint(0, 9))
            while randPos == self.doorPos or randPos in agentAdj or self.map[randPos[0]][randPos[1]].getPit() or self.map[randPos[0]][randPos[1]].getGold():
                randPos = (rd.randint(0, 9), rd.randint(0, 9))
            self.map[randPos[0]][randPos[1]].setGold()
        
        # Add wumpus
        self.numWumpus = numWumpus
        for i in range(self.numWumpus):
            randPos = (rd.randint(0, 9), rd.randint(0, 9))
            while randPos == self.doorPos or randPos in agentAdj or self.map[randPos[0]][randPos[1]].getPit() or self.map[randPos[0]][randPos[1]].getWumpus():
                randPos = (rd.randint(0, 9), rd.randint(0, 9))
            self.map[randPos[0]][randPos[1]].setWumpus()
            adj = self.getAdjacents(randPos[0], randPos[1])
            for a in adj:
                (self.map[a[0]][a[1]]).setStench()

        # Create matrix
        tiles = []
        for i in range(10):
            row = []
            for j in range(10):
                tile = self.map[i][j]
                text = ""
                if tile.getGold(): text = text + 'G'
                if tile.getWumpus(): text = text + 'W'
                if tile.getPit(): text = text + 'P'
                if tile.getBreeze(): text = text + 'B'
                if tile.getStench(): text = text + 'S'
                if tile.getPlayer(): text = text + 'A'
                if text == "":
                    text = '-'
                row.append(text)
            tiles.append(row)
        self.matrix = np.array(tiles)

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