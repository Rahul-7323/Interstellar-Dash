from ursina import *

# shaders are responsible for calculating the levels of lights and darkness of each pixel during the rendering of a 3D scene
from ursina.shaders import lit_with_shadows_shader

# import the player entity from the player.py file
from player import Player
from enclosure import Enclosure
from wall import Wall

# defines the speed of the game
# when training the RL model, the game speed will be set to a higher value
from constants import GAME_SPEED

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

player = Player(parent = scene)

enclosures = [Enclosure(parent = scene, position=(0, 0, 0), scale=(16, 0, 64)), Enclosure(parent = scene, position=(0, 0, 64), scale=(16, 0, 64))]

def update():
    hit_info = enclosures[1].hit_info

    if hit_info and hit_info.entity == player:
        new_enclosure = Enclosure(
            position = (0, 0, enclosures[1].ground.position.z + 64),
            scale = (16, 0, 64)
        )

        destroy(enclosures[0])
        enclosures[0] = enclosures[1]
        enclosures[1] = new_enclosure

editor_camera = EditorCamera(enabled=False, ignore_paused=True)

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

camera.position = (0, 6, -30)

sun = DirectionalLight()
sun.look_at(Vec3(0, -1, -0.75))

app.run()