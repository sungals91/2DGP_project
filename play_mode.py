
from pico2d import *
import game_framework

import game_world
import player
from background import Background
from player import Player

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():

    background = Background()
    game_world.add_object(background, 0)

    player = Player()
    game_world.add_object(player, 1)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass