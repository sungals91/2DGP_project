from pico2d import *
import game_framework

import game_world
from player import Player
from background import Background
from floor import Floor
from skeleton import Skeleton

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
    global player

    background = Background()
    game_world.add_object(background, 0)

    floor = Floor()
    game_world.add_object(floor, 0)

    player = Player()
    game_world.add_object(player, 1)

    skeleton = Skeleton()
    game_world.add_object(skeleton, 1)



    # 충돌 처리물 등록
    game_world.add_collision_pair('player:floor', player, floor)

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass