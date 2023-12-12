import enum
from world import *

class Action(enum.Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    SHOOT = 5
    GRAB = 6
    CLIMB = 7

class Agent:
    def __init__(self, world):
        self.world = world
        self.asset = None
        self.pos = self.world.doorPos
        self.visited = []
        self.action = Action.RIGHT

        # If guiding_path is not empty, this is the action which will be perform when the agent arrives at the end of guiding_path.
        self.guiding_path = []
        # If the agent's previous action is shooting, this is the target of that shot.
        self.prev_shoot_pos = ()