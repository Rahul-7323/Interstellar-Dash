from ursina import *
from random import random
from constants import GAME_SPEED, FORWARD_SPEED

class Wall(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cells = [
            [
                Entity(
                    parent = self,
                    model = 'plane', 
                    position = (-6 + 4*x, 14 - 4*y, 0),
                    collider = 'box', 
                    scale = (4, 0, 4), 
                    texture = 'brick', 
                    texture_scale = (1, 1),
                    rotation_x = -90,
                    enabled = random() > 0.2
                )
                for x in range(4)
            ]
            for y in range(4)
        ]

        self.speed = FORWARD_SPEED