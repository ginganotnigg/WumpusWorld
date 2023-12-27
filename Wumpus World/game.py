from world import *
from agent import *
import pygame
from btn_text import *



# INIT


# CONSTANTS
pt = 70
WIDTH = 10
HEIGHT = 10
stop = False
pause = False
menuBtn = None


# GAME
class Game:
    def __init__(self, world):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH * pt, HEIGHT * pt + 50])
        self.map_font = pygame.font.Font('font/wormcuisine.ttf', 14)
        self.alert_font = pygame.font.Font('font/wormcuisine.ttf', 36)
        self.blur_surface = pygame.Surface((WIDTH * pt, HEIGHT * pt), pygame.SRCALPHA)
        self.fog_surface = pygame.image.load(f'assets/dust.png')
        self.fog_surface = self.fog_surface.convert()
        self.fog_surface.set_alpha(100)
        pygame.display.set_caption('WUMPUS WORLD')

        # Map variables
        self.world = world
        self.tiles = []
        self.objects = []
        self.warnings = []
        self.fog = []

        # Agent
        self.agent = Agent(self.world)

        # Score
        self.score = 0
        self.pauseBtn = None
        self.resumeBtn = None

        # Load images
        self.DOOR = pygame.transform.scale(pygame.image.load(f'assets/door.png'), (pt, pt))
        self.TILE = pygame.transform.scale(pygame.image.load(f'assets/floor.png'), (pt, pt))
        self.WUMPUS = pygame.transform.scale(pygame.image.load(f'assets/monster.png'), (pt, pt))
        self.GOLD = pygame.transform.scale(pygame.image.load(f'assets/gold.png'), (pt, pt))
        self.PIT = pygame.transform.scale(pygame.image.load(f'assets/pit.png'), (pt, pt))
        self.FOG = pygame.transform.scale(self.fog_surface, (pt, pt))
        self.AGENT_DOWN = pygame.transform.scale(pygame.image.load(f'assets/agent_down.png'), (pt, pt))
        self.AGENT_UP = pygame.transform.scale(pygame.image.load(f'assets/agent_up.png'), (pt, pt))
        self.AGENT_LEFT = pygame.transform.scale(pygame.image.load(f'assets/agent_left.png'), (pt, pt))
        self.AGENT_RIGHT = pygame.transform.scale(pygame.image.load(f'assets/agent_right.png'), (pt, pt))
        self.ARROW_DOWN = pygame.transform.scale(pygame.image.load(f'assets/arrow_down.png'), (pt, pt))
        self.ARROW_UP = pygame.transform.scale(pygame.image.load(f'assets/arrow_up.png'), (pt, pt))
        self.ARROW_LEFT = pygame.transform.scale(pygame.image.load(f'assets/arrow_left.png'), (pt, pt))
        self.ARROW_RIGHT = pygame.transform.scale(pygame.image.load(f'assets/arrow_right.png'), (pt, pt))

        # Init blocking view
        for i in range(HEIGHT):
            bRow = []
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if currTile.getPlayer():
                    bRow.append(None)
                else:
                    bRow.append(self.screen.blit(self.FOG, (j * pt, i * pt)))
            self.fog.append(bRow)

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

        # Write warning texts
        for i in range(HEIGHT):
            wRow = []
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if currTile.getBreeze():
                    wRow.append(self.screen.blit(self.map_font.render('Breeze', True, 'white'), (18 + j * pt, 20 + i * pt)))
                if currTile.getStench():
                    wRow.append(self.screen.blit(self.map_font.render('Stench', True, 'white'), (18 + j * pt, 36 + i * pt)))
                if not currTile.getBreeze() and not currTile.getStench():
                    wRow.append(None)
            self.warnings.append(wRow)

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

        # Set blocking view
        for i in range(HEIGHT):
            for j in range(WIDTH):
                currTile = self.world.map[i][j]
                if not currTile.getPlayer() and self.fog[i][j]:
                    self.screen.blit(self.FOG, (j * pt, i * pt))
        
        
    def drawScore(self):
        self.screen.blit(self.alert_font.render(f'Score: {self.score}', True, 'white'), (520, 710))
        self.pauseBtn = Button("PAUSE", 40, 710, True, self.alert_font, self.screen, 'darkslategray' if pause else 'teal')
        self.resumeBtn = Button("RESUME", 150, 710, True, self.alert_font, self.screen, 'darkslategray' if not pause else 'teal')

    def drawAgent(self, cur_step):
        path = self.agent.path
        agentImage = None
        if(cur_step > 0):    
            if path[cur_step][0] > path[cur_step -  1][0]:
                agentImage = self.AGENT_DOWN
            elif path[cur_step][0] < path[cur_step -  1][0]:
                agentImage = self.AGENT_UP
            elif path[cur_step][1] > path[cur_step -  1][1]:
                agentImage = self.AGENT_RIGHT
            elif path[cur_step][1] < path[cur_step -  1][1]:
                agentImage = self.AGENT_LEFT
        else:
            agentImage = self.AGENT_RIGHT
        self.screen.blit(agentImage, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))
        
            
    def turnAgent(self, cur_step):
        path = self.agent.path
        agentImage = None
        if(cur_step > 0) & (cur_step != len(path) - 1):
            if path[cur_step][0] > path[cur_step +  1][0]:
                agentImage = self.AGENT_UP
            elif path[cur_step][0] < path[cur_step +  1][0]:
                agentImage = self.AGENT_DOWN
            elif path[cur_step][1] > path[cur_step +  1][1]:
                agentImage = self.AGENT_LEFT
            elif path[cur_step][1] < path[cur_step +  1][1]:
                agentImage = self.AGENT_RIGHT
            self.screen.blit(agentImage, (self.agent.pos[1] * pt, self.agent.pos[0] * pt))
            
            
    def drawArrow(self, cur_step):
        path = self.agent.path
        actions = self.agent.actions
        if cur_step < len(path) - 1:
            next_pos = path[cur_step + 1]
            if self.world.map[next_pos[0]][next_pos[1]].getWumpus():
                if path[cur_step][0] > next_pos[0]:
                    self.screen.blit(self.ARROW_UP, (next_pos[1] * pt, next_pos[0] * pt))
                elif path[cur_step][0] < next_pos[0]:
                    self.screen.blit(self.ARROW_DOWN, (next_pos[1] * pt, next_pos[0] * pt))
                elif path[cur_step][1] > next_pos[1]:
                    self.screen.blit(self.ARROW_LEFT, (next_pos[1] * pt, next_pos[0] * pt))
                elif path[cur_step][1] < next_pos[1]:
                    self.screen.blit(self.ARROW_RIGHT, (next_pos[1] * pt, next_pos[0] * pt))
                self.world.killWumpus(next_pos[0], next_pos[1])
                self.score -= 100
                if self.fog[next_pos[0]][next_pos[1]]:
                    self.fog[next_pos[0]][next_pos[1]] = None
                
        elif cur_step == len(path) - 1:
            if actions[-1] == Action.SHOOT:
                last_turn = None
                last_action = len(actions) - 1
                while last_action >= 0:
                    if(actions[last_action] in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]):
                        last_turn = actions[last_action]
                        break
                if last_turn == Action.UP:
                    self.screen.blit(self.ARROW_UP, (next_pos[1] * pt, next_pos[0] * pt))
                elif last_turn == Action.DOWN:
                    self.screen.blit(self.ARROW_DOWN, (next_pos[1] * pt, next_pos[0] * pt))
                elif last_turn == Action.LEFT:
                    self.screen.blit(self.ARROW_LEFT, (next_pos[1] * pt, next_pos[0] * pt))
                elif last_turn == Action.RIGHT:
                    self.screen.blit(self.ARROW_RIGHT, (next_pos[1] * pt, next_pos[0] * pt))
                self.score -= 100
        
    ############################# ACTIONS #############################
    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] < HEIGHT and pos[1] >= 0 and pos[1] < WIDTH
    

    def grabGold(self):
        if self.world.map[self.agent.pos[0]][self.agent.pos[1]].getGold():
            self.score += 100
            # UPDATE WORLD
            self.world.grabGold(self.agent.pos[0], self.agent.pos[1])
            # UPDATE game
            self.objects[self.agent.pos[0]][self.agent.pos[1]] = None


    def endGame(self, reason):
        global menuBtn
        self.blur_surface.fill((0, 0, 0, 150))
        self.screen.blit(self.blur_surface, (0, 0))
        alertText = self.alert_font.render('GAME ENDED', True, 'white')
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

        reasonText = self.alert_font.render(reasonStr, True, 'white')
        self.screen.blit(reasonText, reasonText.get_rect(center=(WIDTH * pt // 2, HEIGHT * pt // 2 + 20)))
        menuBtn = Button("MAIN MENU", 40, 40, True, self.alert_font, self.screen, width=150)
            

    def removeWumpus(self, pos):
        if self.validPos(pos):
            self.world.numWumpus -= 1
            self.world.map[pos[0]][pos[1]].removeWumpus()
            if self.validPos((pos[0] + 1, pos[1])):
                pos_ = (pos[0] + 1, pos[1])
                self.world.map[pos_[0]][pos_[1]].removeStench()
            if self.validPos((pos[0] - 1, pos[1])):
                pos_ = (pos[0] - 1, pos[1])
                self.world.map[pos_[0]][pos_[1]].removeStench()
            if self.validPos((pos[0], pos[1] + 1)):
                pos_ = (pos[0], pos[1] + 1)
                self.world.map[pos_[0]][pos_[1]].removeStench()
            if self.validPos((pos[0], pos[1] - 1)):
                pos_ = (pos[0], pos[1] - 1)
                self.world.map[pos_[0]][pos_[1]].removeStench()

            
    def removePlayer(self, position):
        if self.validPos(position):
            self.world.map[position[0]][position[1]].removePlayer()


    ############################# UPDATE GAME #############################
            
    def updateMap(self, current_step):
        global stop, pause
        next_pos = self.agent.path[current_step]
        self.agent.update_position(next_pos)
        if self.fog[next_pos[0]][next_pos[1]]:
            self.fog[next_pos[0]][next_pos[1]] = None
        if not stop and not pause: self.score -= 10
        self.grabGold()
        if not self.world.leftWumpus() and not self.world.leftGold():
            stop = True
        if current_step == len(self.agent.path) - 1 or self.agent.actions[-1] == Action.CLIMB:
            if not stop and not pause: self.score += 10
            stop = True

    def updateEnd(self):
        pygame.time.delay(1000)
        if not self.world.leftWumpus() and not self.world.leftGold():
            self.endGame("Clear")
        else: self.endGame("Climb")


    

# EXECUTE
def run_game_screen(state, selected_level):
    global stop, pause
    if stop: stop = False
    wumpus_map = WumpusWorld()
    wumpus_map.readMap(f'map/map{selected_level}.txt')
    game = Game(wumpus_map)

    game.agent.get_actions_list()
    game.agent.get_move_action()
    agent_actions = game.agent.actions
    agent_path = game.agent.path
    current_step = 0
    run = True
    
    while run:
        game.screen.fill('black')

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                state['execute'] = False
            if not stop and game.pauseBtn and game.pauseBtn.is_clicked(event):
                pause = True
            if not stop and game.resumeBtn and game.resumeBtn.is_clicked(event):
                pause = False
            if menuBtn is not None and menuBtn.is_clicked(event):
                state['inGame'] = not state['inGame']
                return
            
        # Update world
        game.updateMap(current_step)
        game.drawWorld()
        game.drawScore()
        game.drawAgent(current_step)
        if not stop and not pause:
            pygame.display.flip()
            pygame.time.delay(100)
            game.turnAgent(current_step)
            game.drawArrow(current_step)
            current_step += 1
        elif stop:
            game.updateEnd()

        pygame.display.flip()
        pygame.time.delay(200)
    pygame.quit()

#run_game_screen(state=None, selected_level=2)