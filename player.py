from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

player = FirstPersonController(model = 'cube', z = -10, color = color.orange, origin_y = -0.5, speed = 8, collider = 'box')
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

# class Player(FirstPersonController):
#   def __init__(self, *args, **kwargs):
#     super().__init__(model = 'cube', z = -10, color = color.orange, origin_y = -0.5, speed = 8, collider = 'box', *args, **kwargs)
#     self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))

# class Player(Entity):
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)

#     self.controller = FirstPersonController(parent = self, model = 'cube', z = -10, color = color.orange, origin_y = -0.5, speed = 8, collider = 'box', *args, **kwargs)
#     self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))
