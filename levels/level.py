from geometry.vector import Vector
from geometry.rectangle import Rectangle

class Level:
    def __init__(self, level_id, start_pos, target, bounds, platforms, kill_boxes):
        self.level_id = level_id
        self.start_pos = start_pos
        self.target = target
        self.bounds = bounds
        self.platforms = platforms
        self.kill_boxes = kill_boxes