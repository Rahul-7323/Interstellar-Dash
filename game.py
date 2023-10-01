from ursina import *

# shaders are responsible for calculating the levels of lights and darkness of each pixel during the rendering of a 3D scene
from ursina.shaders import lit_with_shadows_shader

# import the player entity from the player.py file
from player import Player
from enclosure import Enclosure

# defines the speed of the game
# when training the RL model, the game speed will be set to a higher value
from constants import GAME_SPEED

Entity.default_shader = lit_with_shadows_shader

class Game(Entity):
    def __init__(self):
        super().__init__()

        self.score = 0

        self.enclosures = [Enclosure(parent = self, position=(0, 0, 32), scale=(16, 0, 64)), Enclosure(parent = self, position=(0, 0, 96), scale=(16, 0, 64))]

        # Black screen that obstructs the next enclosure
        self.black_screen = Entity(
            parent = self,
            model = 'plane', 
            position = (0, 8, 40),
            collider = 'box', 
            scale = (16, 0, 16), 
            texture_scale = (1, 1),
            rotation_x = -90,
            color = color.black66
        )

        self.player = Player(parent = self)
    
    def update(self):
        hit_info = self.enclosures[1].hit_info

        if hit_info and hit_info.entity == self.player:
            self.score += 1

            new_enclosure = Enclosure(
                parent = self,
                position = (0, 0, self.enclosures[1].ground.position.z + 64),
                scale = (16, 0, 64)
            )

            destroy(self.enclosures[0])
            self.enclosures[0] = self.enclosures[1]
            self.enclosures[1] = new_enclosure