import enum
import numpy as np
import world


class Action(enum.Enum):
    #GO = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    #
    SHOOT = 5
    GRAB = 6
    CLIMB = 7

class Agent:
    def __init__(self, world_class):
        #
        self.world = world_class.matrix
        self.start = world_class.doorPos
        ##
        self.B = np.full_like(self.world, 0, dtype=int)
        self.P = np.full_like(self.world, 0, dtype=int)
        self.S = np.full_like(self.world, 0, dtype=int)
        self.W = np.full_like(self.world, 0, dtype=int)
        ##
        self.visited = []
        self.safe = [self.start]
        self.safe.extend(self.adj(self.start))
        self.stack = [self.start]
        self.prev = {}
        ##
        self.path = []
        self.actions = [Action.RIGHT]
        self.num_gold = 0
        self.ramify = []
        self.shooting_position = []
        self.pos = (0, 0)
        # If guiding_path is not empty, this is the action which will be perform when the agent arrives at the end of guiding_path.
        #self.guiding_path = []
        # If the agent's previous action is shooting, this is the target of that shot.
        #self.prev_shoot_pos = ()

    def update_position(self, next_position):
        self.pos = next_position
        
    def adj(self, x): #adjacent cells of x
        arr = []
        i = x[0]
        j = x[1]
        if i - 1 >= 0:
            arr.append((i - 1, j))
        if j - 1 >= 0:
            arr.append((i, j - 1))
        if i + 1 <= len(self.world) - 1:
            arr.append((i + 1, j))
        if j + 1 <= len(self.world) - 1:
            arr.append((i, j + 1))
        return arr

    def update_map(self, x): #update the map with the newly-known x
        for i in range(len(self.world) - 1):
            for j in range(len(self.world) - 1):
                if at(self.B,(i, j)) == 1 and at(self.S,(i, j)) == 0 and at(self.B,(i+1, j+1)) == 0 and at(self.S,(i+1, j+1)) == 1:
                    set(self.P,(i, j + 1),0) 
                    set(self.W,(i, j + 1),0) 
                    set(self.P,(i + 1, j),0) 
                    set(self.W,(i + 1, j),0)
                    if (i, j + 1) not in self.safe:
                        self.safe.append((i, j + 1))
                    if (i + 1, j) not in self.safe:
                        self.safe.append((i + 1, j))
            for j in range(1, len(self.world)):
                if at(self.B,(i, j)) == 1 and at(self.S,(i, j)) == 0 and at(self.B,(i+1, j-1)) == 0 and at(self.S,(i+1, j-1)) == 1:
                    set(self.P,(i, j - 1),0) 
                    set(self.W,(i, j - 1),0) 
                    set(self.P,(i + 1, j),0) 
                    set(self.W,(i + 1, j),0)
                    if (i, j - 1) not in self.safe:
                        self.safe.append((i, j - 1))
                    if (i + 1, j) not in self.safe:
                        self.safe.append((i + 1, j))

            #wumpus detection
            for j in range(1, len(self.world)):
                if at(self.S,(i,j)) == 1:
                    not_wumpus = []
                    for cell in self.adj((i,j)):
                        if at(self.P,cell) == 1 or cell in self.visited or cell in self.safe:
                            not_wumpus.append(cell)
                    temp = len(self.adj((i,j))) - 1
                    if len(not_wumpus) == temp: #make sure that all-except-one adjacent cell is safe, the remaining cell is the wumpus
                        for cell in self.adj((i,j)): 
                            if cell not in not_wumpus:
                                set(self.W,cell,1)
                                if (i,j) not in self.shooting_position: 
                                    self.shooting_position.append((i,j))
                                    #make the bfs path from here to the shooting position NOT VISITED to make the agent go there again to shoot the wumpus
                                    bfs_path = self.goback_bfs(x, (i,j))
                                    for cell in bfs_path:
                                        if cell in self.visited:
                                            self.visited.remove(cell)


    def update_ramify(self): #update the intersections that can be backtracked
        for i in self.ramify:
            num_visit = 0
            for j in self.adj(i):
                if (j in self.visited) or (j not in self.safe):
                    num_visit += 1
            if num_visit >= len(self.adj(i)):
                self.ramify.remove(i)
    
    # def update_stack(self):
    #     pass
    #         for i in self.stack:
    #          if (at(self.W,i) == 1) or (at(self.P,i) == 1):
    #              self.stack.remove(i)

    def goback_bfs(self, start, end):
        parent = {}
        queue = [start]
        bfs_visited = []
        bfs_path = []
        while len(queue) > 0:
            browse_cur = queue[0]
            bfs_visited.append(browse_cur)
            queue = queue[1:]
            if browse_cur == end:
                bfs_path = [end]
                while bfs_path[-1] != start:
                    bfs_path.append(parent[bfs_path[-1]])
                bfs_path.reverse()
                return bfs_path[1:]
            for adjacent in self.adj(browse_cur):
                if (adjacent not in queue) and (adjacent in self.safe) and (adjacent not in bfs_visited):
                    parent[adjacent] = browse_cur
                    queue.append(adjacent)
    
    def get_move_action(self):
        if len(self.path) < 2:
            return
        old_x = self.path[-2] [0]
        old_y = self.path[-2] [1]
        new_x = self.path[-1] [0]
        new_y = self.path[-1] [1]
        i = 1
        while (not_moving_action(self.actions[-i])): #take the latest actions that are NOT special actions (shoot, grab)
            i += 1
        latest_dir = self.actions[-i]
        ##
        if new_x < old_x:
            self.actions.append(Action.UP)
            if latest_dir != Action.UP: 
                self.actions.append(Action.UP)
        if new_x > old_x:
            self.actions.append(Action.DOWN)
            if latest_dir != Action.DOWN: 
                self.actions.append(Action.DOWN)
        if new_y < old_y:
            self.actions.append(Action.LEFT)
            if latest_dir != Action.LEFT: 
                self.actions.append(Action.LEFT)
        if new_y > old_y:
            self.actions.append(Action.RIGHT)
            if latest_dir != Action.RIGHT: 
                self.actions.append(Action.RIGHT)

    def shoot(self,cur):
        for wumpus in self.adj(cur):
            if at(self.W,wumpus) == 1:
                x = cur[0]
                y = cur[1]
                wx = wumpus[0]
                wy = wumpus[1]
                if (wx > x): self.actions.append(Action.DOWN)
                elif (wx < x): self.actions.append(Action.UP)
                elif (wy > y): self.actions.append(Action.RIGHT)
                elif (wy < y): self.actions.append(Action.LEFT)
                self.actions.append(Action.SHOOT)
                #remove wumpus and its stench and remove shooting positions around
                set(self.W,wumpus,0)
                self.safe.append(wumpus)
                for cell in self.adj(wumpus):
                    #remove one stench
                    temp = at(self.world,cell)
                    temp = temp.replace('S','',1)
                    set(self.world,cell,temp)
                    ##make unvisited
                    # if cell in self.visited:
                    #     self.visited.remove(cell)
                    #remove shooting pos
                    # if cell in self.shooting_position:
                    #     self.shooting_position.remove(cell)

#GET THE LIST OF ACTIONS/PATH
    def get_actions_list(self):
        while len(self.stack) != 0:
            #self.update_stack()
            cur = self.stack[-1]
            self.stack = self.stack[:-1]
            if at(self.world,cur) == '-':
                for i in self.adj(cur):
                    if i not in self.safe:
                        self.safe.append(i)
            if cur not in self.visited:
                ##
                self.path.append(cur)
                self.get_move_action()
                self.visited.append(cur)
                ##
                if 'G' in at(self.world,cur):
                    self.num_gold += 1
                    self.actions.append(Action.GRAB)
                if 'B' in at(self.world,cur):
                    set(self.B,cur,1)
                    if cur not in self.safe:
                        self.safe.append(cur)
                if 'S' in at(self.world,cur):
                    set(self.S,cur,1)
                    if cur not in self.safe:
                        self.safe.append(cur)
                    if cur in self.shooting_position:
                        self.shoot(cur)
                self.update_map(cur)
                self.update_ramify()
                ##
                num_direc = 0
                for i in self.adj(cur):
                    if (i not in self.visited) & (i in self.safe):
                        self.stack.append(i)
                        self.prev[i] = cur
                        num_direc += 1
                if num_direc > 1:
                    self.ramify.append(cur)
                elif num_direc == 0: 
                    self.update_ramify()
                    bfs_path = []
                    if len(self.ramify) > 0:
                        bfs_path = self.goback_bfs(cur, self.ramify[-1])
                        if type(bfs_path)!=None: 
                            for step in bfs_path:
                                self.path.append(step)
                                self.get_move_action()
                    else:
                        bfs_path = self.goback_bfs(cur, self.start)
                        if type(bfs_path)!= None: 
                            for step in bfs_path:
                                self.path.append(step)
                                self.get_move_action()
                        break
            #print(self.safe)
            # print(self.path)
            self.actions.append(Action.CLIMB)
            
def not_moving_action(act):
    return (act == Action.CLIMB) or (act == Action.SHOOT) or (act == Action.GRAB)

def at(m,coor):
    x = coor[0]
    y = coor[1]
    return m[x][y]
def set(m,coor,val):
    x = coor[0]
    y = coor[1]
    m[x][y] = val



# class TestWorld:
#     def __init__(self):
#         self.doorPos = (9,0)
#         self.map = []
#         with open('map1.txt', 'r') as f:
#             lines = f.read().splitlines()
#             for line in lines:
#                 (self.map).append(line.split('.'))
#         print(self.map)

# test = TestWorld()
# agent = Agent(test.map,test.doorPos)

# agent.get_actions_list()
# print(agent.actions)
# print(agent.path)
