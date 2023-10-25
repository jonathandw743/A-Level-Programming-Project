from .camera import Camera
from .player import Player
import pygame


class GameState:
    def __init__(self, level):
        self.player = Player(
            level.start_pos.x, level.start_pos.y, 0.5, 0.5, vel_x=0, vel_y=0
        )

    def respawn(self, level):
        self.player = Player(
            level.start_pos.x, level.start_pos.y, 0.5, 0.5, vel_x=0, vel_y=0
        )

    def update(self, player):
        self.player = player

    def get(self):
        return (self.player)