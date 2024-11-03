from pico2d import *

from Player import Player


class Floor:
    image = None
    def __init__(self):
        self.x, self.y = 0, 200
        if Floor.image == None:
            Floor.image = load_image('image//tile.png')
    def update(self):
        pass
    def draw(self):
        for i in range(13):
            self.image.clip_draw(0,220,70,20,self.x + i*70,self.y)
        pass

class Background:
    image = None

    def __init__(self):
        self.x, self.y = 0, 0
        if Background.image == None:
            Background.image = load_image('image\\wall.png')
    def update(self):
        pass
    def draw(self):
        for i in range(6):
            for k in range(7):
                self.image.draw(self.x + k*128, self.y + i*128)


def reset_world():
    global running
    global world
    global player
    global background
    global floor

    running = True
    world = []

    background = Background()
    world.append(background)

    floor = Floor()
    world.append(floor)

    player = Player()
    world.append(player)


    pass

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type in (SDL_KEYDOWN, SDL_KEYUP):
            player.handle_event(event)
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False
    pass

open_canvas()

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

# finalization code
close_canvas()