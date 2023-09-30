from ursina import *
from random import random, randrange
from constants import GAME_SPEED, FORWARD_SPEED

class Grid(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid = [
            [
                Entity(
                    parent = self,
                    model = 'plane', 
                    position = (-6 + 4*x, 14 - 4*y, 0),
                    collider = 'box', 
                    scale = (4, 1, 4), 
                    texture = 'brick', 
                    texture_scale = (1, 1),
                    rotation_x = -90,
                    enabled = True
                )
                for x in range(4)
            ]
            for y in range(4)
        ]

        disabled_count = 0

        for row in self.grid:
            for cell in row:
                disabled_count += int(not cell.enabled)

        # If all cells are disabled, then choose some random cell
        # and make that enabled
        if disabled_count == 0:
            self.grid[randrange(0, 4)][randrange(0, 4)].enabled = False