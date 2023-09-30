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
        self.speed = 8

        self.height = 1

        camera.fov = 90
        self.mouse_sensitivity = Vec2(40, 40)

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
        if ray.hit:
            self.y = ray.world_point.y
        
        self.position += (0, 0, 0)

        # JUMP PHYSICS VARIABLES
        self.gravity = 60
        self.jump_height = 3
        self.air_time = 0
        self.velocity = 0
        self.prev_y = 0

    def update(self):
        curr_y = self.prev_y + self.calc_position(self.velocity, self.air_time, self.gravity)

        ray = raycast(self.position + (0, self.height/2, 0), self.forward, distance = 0.8, traverse_target=self.traverse_target, ignore=self.ignore_list, debug=True, color=color.yellow)
        # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)
        # if not on ground and not on way up in jump, fall
        # if ray.hit:
        #     print('hit the front wall')
        if ray.hit:
            print('hit something')

        if curr_y <= 0:
            self.air_time = 0
            self.velocity = 0
            self.prev_y = 0
        elif curr_y + self.height/2 >= 16:
            self.air_time = time.dt * GAME_SPEED
            self.velocity = 0
            self.prev_y = self.y
        else:
            self.y = curr_y
            self.air_time += time.dt * GAME_SPEED

        self.direction = Vec3(self.right * (held_keys['d'] - held_keys['a'])).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        
        if not feet_ray.hit and not head_ray.hit:
            move_amount = (self.direction * time.dt * GAME_SPEED * self.speed)

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
        
            self.position += move_amount


    def calc_velocity(self, height, gravity):
        return sqrt(2 * height * gravity)
    
    def calc_position(self, initial_velocity, time, gravity):
        return (initial_velocity * time) - (gravity * time**2) / 2

    def input(self, key):
        if key == 'space':
            self.jump()
    
    def jump(self):
        self.velocity = self.calc_velocity(self.jump_height, self.gravity)
        self.air_time = time.dt * GAME_SPEED
        self.prev_y = self.y