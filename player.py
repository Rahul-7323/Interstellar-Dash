from ursina import *
from constants import GAME_SPEED

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))
        self.model = 'sphere'
        self.z = -10
        self.color = color.orange
        self.origin_y = -0.5
        self.speed = 8 * GAME_SPEED

        self.height = 2

        camera.fov = 90
        mouse.locked = False
        self.mouse_sensitivity = Vec2(40, 40)

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
        if ray.hit:
            self.y = ray.world_point.y

        # JUMP PHYSICS VARIABLES
        self.gravity = 40 * GAME_SPEED
        self.jump_height = 2 

    def update(self):
        self.direction = Vec3(self.right * (held_keys['d'] - held_keys['a'])).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

        # gravity
        ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
        # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)
        # if not on ground and not on way up in jump, fall

    def input(self, key):
        if key == 'w' and self.y <= 16:
            self.jump()

    # function to find the time taken for a ball to reach a given height 
    # when thrown vertically upward under gravity g
    def fall_duration(self, height):
        return sqrt((2 * height) / self.gravity)

    def jump(self):
        if hasattr(self, 'y_animator'):
            self.y_animator.pause()

        duration = self.fall_duration(self.jump_height)
        print(self.y)
        self.animate_y(self.y+self.jump_height, duration, resolution=int(1//time.dt), curve=curve.out_quad, auto_destroy = True)
        invoke(self.start_fall, delay=duration-0.1)

    def start_fall(self):
        self.y_animator.pause()
        self.animate_y(0, self.fall_duration(self.y), resolution=int(1//time.dt), curve=curve.in_quad, auto_destroy = True)

    def on_enable(self):
        mouse.locked = True

    def on_disable(self):
        mouse.locked = False