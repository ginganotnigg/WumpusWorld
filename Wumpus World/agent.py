import enum

class Action(enum.Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    SHOOT = 5
    GRAB = 6
    CLIMB = 7

class Agent:
    def __init__(self, start_pos):
        self.asset = None
        self.START = start_pos
        self.pos = self.START
        self.visited = []
        self.action = Action.RIGHT

        # If guiding_path is not empty, this is the action which will be perform when the agent arrives at the end of guiding_path.
        self.guiding_path = []
        # If the agent's previous action is shooting, this is the target of that shot.
        self.prev_shoot_pos = ()
        
    def update_position(self, next_position):
        self.pos = next_position