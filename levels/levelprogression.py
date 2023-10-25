from geometry.vector import Vector
from game.gamestate import GameState

class LevelProgression:
    def __init__(self, level):
        self.completed = False
        self.game_state = GameState(level)