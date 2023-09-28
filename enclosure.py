from ursina import *
from constants import GAME_SPEED

class Enclosure(Entity):
    def __init__(self, position, scale, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # you have to set the parent entity to be equal to self, or else
        # when you destroy an instance of Enclosure, the ground entity won't
        # get destroyed along with it
        self.ground = Entity(
            parent = self,
            model = 'plane', 
            position = position,
            collider = 'box', 
            scale = scale, 
            texture = 'brick', 
            texture_scale = (4, 4)
        )

        self.left_wall = Entity(
            parent = self,
            model = 'plane',
            position = (position[0] - 8, position[1] + 8, position[2]),
            collider = 'box',
            scale = scale,
            texture = 'brick',
            texture_scale = (6, 6),
            rotation_z = 90
        )

        self.right_wall = Entity(
            parent = self,
            model = 'plane',
            position = (position[0] + 8, position[1] + 8, position[2]),
            collider = 'box',
            scale = scale,
            texture = 'brick',
            texture_scale = (6, 6),
            rotation_z = -90
        )

        self.ceiling = Entity(
            parent = self,
            model = 'plane', 
            position = (position[0], position[1] + 16, position[2]),
            collider = 'box', 
            scale = scale, 
            texture = 'brick', 
            texture_scale = (4, 4),
            rotation_z = 180
        )

        self.hit_info = None
        
        self.speed = 40

    def update(self):
        self.ground.z -= time.dt * self.speed * GAME_SPEED
        self.left_wall.z -= time.dt * self.speed * GAME_SPEED
        self.right_wall.z -= time.dt * self.speed * GAME_SPEED
        self.ceiling.z -= time.dt * self.speed * GAME_SPEED

        self.hit_info = boxcast(
            self.ground.position,
            direction=(0,1,0), 
            distance=16, 
            thickness=(self.ground.scale.x, self.ground.scale.z/2), 
            ignore=[self.ground], 
            debug=False
        )
    