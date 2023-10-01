from ursina import *
from game import Game

app = Ursina()

game = Game()

score_entity = Text(f'SCORE: 0', color = color.green, origin = (6, -16), background = color.black)
score_entity.create_background()

def update():
    global game

    if game.player.hit_grid:
        destroy(game)
        game = Game()

    score_entity.text = f'SCORE: {game.score}'
    score_entity.create_background()

editor_camera = EditorCamera(enabled=False, ignore_paused=True)

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        mouse.locked = not editor_camera.enabled
        # editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

camera.position = (0, 6, -30)

# sun = DirectionalLight()
# sun.look_at(Vec3(0, -1, 0))
app.run()