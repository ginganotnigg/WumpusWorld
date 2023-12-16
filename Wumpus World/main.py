from world import *
from agent import *
# from logic import get_agent_path
import pygame
import enum


# INIT
pygame.init()



# CONSTANTS
pt = 70
WIDTH = 10
HEIGHT = 10
map_font = pygame.font.Font('freesansbold.ttf', 14)
alert_font = pygame.font.Font('freesansbold.ttf', 30)
run = True
stop = False



# BOARD
class Board:
    

    def __init__(self, world):
        self.screen = pygame.display.set_mode([WIDTH * pt, HEIGHT * pt + 50])
        pygame.display.set_caption('WUMPUS WORLD')

        # Map variables
        self.world = world
        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []

        # Agent
        self.agent = Agent(self.world.doorPos)

        # Score
        self.score = 0

        # Load images
        self.DOOR = pygame.transform.scale(pygame.image.load(f'assets/door.png'), (pt, pt))
        self.TILE = pygame.transform.scale(pygame.image.load(f'assets/floor.png'), (pt, pt))
        self.WUMPUS = pygame.transform.scale(pygame.image.load(f'assets/wumpus.png'), (pt, pt))
        self.GOLD = pygame.transform.scale(pygame.image.load(f'assets/gold.png'), (pt, pt))
        self.PIT = pygame.transform.scale(pygame.image.load(f'assets/pit.png'), (pt, pt))
        self.TERRAIN = pygame.transform.scale(pygame.image.load(f'assets/terrain.png'), (pt, pt))
        self.AGENT_DOWN = pygame.transform.scale(pygame.image.load(f'assets/agent_down.png'), (pt, pt))
        self.AGENT_UP = pygame.transform.scale(pygame.image.load(f'assets/agent_up.png'), (pt, pt))
        self.AGENT_LEFT = pygame.transform.scale(pygame.image.load(f'assets/agent_left.png'), (pt, pt))
        self.AGENT_RIGHT = pygame.transform.scale(pygame.image.load(f'assets/agent_right.png'), (pt, pt))
        self.ARROW_DOWN = pygame.transform.scale(pygame.image.load(f'assets/arrow_down.png'), (pt, pt))
        self.ARROW_UP = pygame.transform.scale(pygame.image.load(f'assets/arrow_up.png'), (pt, pt))
        self.ARROW_LEFT = pygame.transform.scale(pygame.image.load(f'assets/arrow_left.png'), (pt, pt))
        self.ARROW_RIGHT = pygame.transform.scale(pygame.image.load(f'assets/arrow_right.png'), (pt, pt))

    ############################# GRAPHICS #############################

    def drawWorld(self):
        # Create tiles
        for i in range(HEIGHT):
            tRow = []
            for j in range(WIDTH):
                if (i == self.world.doorPos[0] and j == self.world.doorPos[1]):
                    tRow.append(self.screen.blit(self.DOOR, (j * pt, i * pt)))
                else: tRow.append(self.screen.blit(self.TILE, (j * pt, i * pt)))
            self.tiles.append(tRow)

        #Create objects
        for i in range(HEIGHT):
            oRow = []
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if currTile.getPit():
                    oRow.append(self.screen.blit(self.PIT, (j * pt, i * pt)))
                elif currTile.getWumpus():
                    oRow.append(self.screen.blit(self.WUMPUS, (j * pt, i * pt)))
                elif currTile.getGold():
                    oRow.append(self.screen.blit(self.GOLD, (j * pt, i * pt)))
                else:
                    oRow.append(None)
            self.objects.append(oRow)

        # Write warning texts
        for i in range(HEIGHT):
            wRow = []
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if currTile.getBreeze():
                    wRow.append(self.screen.blit(map_font.render('Breeze', True, 'white'), (12 + j * pt, 20 + i * pt)))
                if currTile.getStrench():
                    wRow.append(self.screen.blit(map_font.render('Strench', True, 'white'), (8 + j * pt, 36 + i * pt)))
                if not currTile.getBreeze() and not currTile.getStrench():
                    wRow.append(None)
            self.warnings.append(wRow)

        # Set blocking view
        for i in range(HEIGHT):
            bRow = []
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if currTile.getPlayer():
                    self.agent.pos = (i, j)
                    self.agent.asset = self.screen.blit(self.AGENT_RIGHT, (j * pt, i * pt))
                    bRow.append(self.agent.asset)
                else:
                    pass
                    #bRow.append(self.screen.blit(self.TERRAIN, (j * pt, i * pt)))
            self.terrains.append(bRow)
        
    def drawScore(self):
        self.screen.blit(alert_font.render(f'Score: {self.score}', True, 'white'), (WIDTH * pt / 2 - 80, HEIGHT * pt + 10))

    def drawAgent(self):
        if self.agent.action == Action.UP:
            self.screen.blit(self.AGENT_UP, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))
        elif self.agent.action == Action.LEFT:
            self.screen.blit(self.AGENT_LEFT, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))
        elif self.agent.action == Action.DOWN:
            self.screen.blit(self.AGENT_DOWN, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))
        elif self.agent.action == Action.RIGHT:
            self.screen.blit(self.AGENT_RIGHT, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))


    ############################# ACTIONS #############################
    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] < HEIGHT and pos[1] >= 0 and pos[1] < WIDTH
    
    def moveForward(self, action):
        nextPos = None

        if action == Action.LEFT:
            nextPos = (self.agent.pos[0], self.agent.pos[1] - 1)
        elif action == Action.RIGHT:
            nextPos = (self.agent.pos[0], self.agent.pos[1] + 1)
        elif action == Action.UP:
            nextPos = (self.agent.pos[0] - 1, self.agent.pos[1])
        elif action == Action.DOWN:
            nextPos = (self.agent.pos[0] + 1, self.agent.pos[1])

        if self.validPos(nextPos):
            # Kiểm tra xem ô tiếp theo có Gold không
            nextTile = self.world.map[nextPos[0]][nextPos[1]]
            if nextTile.getGold():
                self.world.grabGold(nextPos[0], nextPos[1])  # Xóa Gold từ bản đồ
                self.score += 100  # Cộng điểm cho việc nhặt Gold

            self.world.movePlayer(self.agent.pos[0], self.agent.pos[1], nextPos[0], nextPos[1])

            self.agent.state = action

            self.score -= 10

            currTile = self.world.map[self.agent.pos[0]][self.agent.pos[1]]
            if currTile.getPit():
                self.score -= 10000
                self.endGame("Pit")
            elif currTile.getWumpus():
                self.score -= 10000
                self.endGame("Wumpus")


    def shootForward(self, action):
        arrow = None
        arrow_img = None
        arrow_loc = None
        if action == Action.LEFT:
            arrow_loc = (self.agent.pos[0], self.agent.pos[1] - 1)
            arrow_img = self.ARROW_LEFT
        elif action == Action.RIGHT:
            arrow_loc = (self.agent.pos[0], self.agent.pos[1] + 1)
            arrow_img = self.ARROW_RIGHT
        elif action == Action.UP:
            arrow_loc = (self.agent.pos[0] - 1, self.agent.pos[1])
            arrow_img = self.ARROW_UP
        elif action == Action.DOWN:
            arrow_loc = (self.agent.pos[0] + 1, self.agent.pos[1])
            arrow_img = self.ARROW_DOWN
        
        self.screen.blit(arrow_img, (arrow_loc[1] * pt, arrow_loc[0] * pt))

        self.score -= 100

        if self.world.map[arrow_loc[0]][arrow_loc[1]].getWumpus():
            # UPDATE WORLD
            self.world.killWumpus(arrow_loc[0], arrow_loc[1])

            # UPDATE BOARD
            #if self.terrains[arrow_loc[0]][arrow_loc[1]]:
                #self.terrains[arrow_loc[0]][arrow_loc[1]] = None

            self.objects[arrow_loc[0]][arrow_loc[1]] = None

            adj = self.world.getAdjacents(arrow_loc[0], arrow_loc[1])
            for a in adj:
                self.warnings[a[0]][a[1]][1] = None

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.endGame("Clear")


    def grabGold(self, action):
        if self.world.map[self.agent.pos[0]][self.agent.pos[1]].getGold():
            self.score += 100

            # UPDATE WORLD
            self.world.grabGold(self.agent.pos[0], self.agent.pos[1])

            # UPDATE BOARD
            self.objects[self.agent.pos[0]][self.agent.pos[1]] = None

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.endGame("Clear")


    def endGame(self, reason):
        global stop
        stop = True
        pygame.draw.rect(self.screen, 'black', pygame.Rect(0, 0, WIDTH * pt, HEIGHT * pt + 50))

        alertText = alert_font.render('GAME ENDED', True, 'white')
        self.screen.blit(alertText, alertText.get_rect(center=(WIDTH * pt // 2, HEIGHT * pt // 2 - 20)))

        reasonStr = None
        if reason == 'Pit':
            reasonStr = 'You fell into a Pit'
        elif reason == 'Wumpus':
            reasonStr = 'You were killed by a Wumpus'
        elif reason == 'Climb':
            reasonStr = 'You climb out of the Cave'
        elif reason == 'Clear':
            reasonStr = 'You cleared the Map'

        reasonText = alert_font.render(reasonStr, True, 'white')
        self.screen.blit(reasonText, reasonText.get_rect(center=(WIDTH * pt // 2, HEIGHT * pt // 2 + 20)))

    ############################# INPUT AND UPDATE GAME #############################
    def removeGold(self, position):
        if self.validPos(position):
            self.world.map[position[0]][position[1]].removeGold()
            # self.objects[position[0]][position[1]] = None
    def removeWumpus(self, position):
        if self.validPos(position):
            self.world.map[position[0]][position[1]].removeWumpus()
            # self.objects[position[0]][position[1]] = None
    def removePlayer(self, position):
        if self.validPos(position):
            self.world.map[position[0]][position[1]].removePlayer()
            # self.objects[position[0]][position[1]] = None
            
    def updateBoard(self, event):
        if event.key == pygame.K_w:
            action = Action.UP
            if action == self.agent.action:
                self.moveForward(action)
            else:
                self.agent.action = action
        if event.key == pygame.K_a:
            action = Action.LEFT
            if action == self.agent.action:
                self.moveForward(action)
            else:
                self.agent.action = action
        if event.key == pygame.K_s:
            action = Action.DOWN
            if action == self.agent.action:
                self.moveForward(action)
            else:
                self.agent.action = action
        if event.key == pygame.K_d:
            action = Action.RIGHT
            if action == self.agent.action:
                self.moveForward(action)
            else:
                self.agent.action = action
        if event.key == pygame.K_f:
            action = Action.SHOOT
            self.shootForward(self.agent.action)
        if event.key == pygame.K_g:
            action = Action.GRAB
            self.grabGold()
        if event.key == pygame.K_c:
            action = Action.CLIMB
            if self.agent.pos == self.world.doorPos:
                self.score += 10
                self.endGame("Climb")
            
def update_agent_position_from_path(agent, board, path, current_step):
    # if path:
    #     next_position = path.pop(0)
        next_position = path[current_step]
        agent.update_position(next_position)

        # Nếu Agent tới vị trí có Gold, thì xóa Gold
        if board.world.map[next_position[0]][next_position[1]].getGold():
            board.removeGold(next_position)
        # Nếu Agent tới vị trí có Wumpus, thì xóa Wumpus
        if board.world.map[next_position[0]][next_position[1]].getWumpus():
            board.removeWumpus(next_position)

agent_path = [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 7), (8, 7), (9, 7), (9, 6), (9, 5), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (6, 2), (6, 1), (6, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (5, 3), (5, 4), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (7, 9), (7, 8), (7, 9), (6, 9), (5, 9), (5, 8), (5, 7), (6, 7), (5, 7), (5, 6), (4, 6), (4, 7), (4, 8), (4, 9), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (3, 5), (2, 5), (3, 5), (3, 6), (3, 7), (2, 7), (2, 8), (2, 9), (1, 9), (1, 8), (1, 7), (1, 6), (0, 6), (0, 7), (0, 8), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (3, 5), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (9, 0)]
current_step = 0

# EXECUTE
wumpus = WumpusWorld()
wumpus.readMap('map/map1.txt')
board = Board(wumpus)
stack = []

board.removePlayer(list(agent_path[0]))

while run and current_step < len(agent_path):
    board.screen.fill('black')
    board.drawWorld()

    # Update agent position
    # board.agent.update_position(agent_path[current_step])
    update_agent_position_from_path(board.agent, board, agent_path, current_step)

    # Draw agent and other elements
    board.drawAgent()
    board.drawScore()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not stop and event.type == pygame.KEYUP:
            board.updateBoard(event)

    pygame.display.flip()
    pygame.time.delay(100)  # Adjust the delay time as needed
    current_step += 1
pygame.quit()
