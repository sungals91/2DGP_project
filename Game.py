from pico2d import *

class Player:
    def __init__(self):
        self.image = load_image('player\Idle.png')
        self.x, self.y = 400, 300
        self.frame = 0
        pass
    def update(self):
        self.frame = (self.frame + 1) % 8
        pass
    def draw(self):
        self.image.clip_draw(self.frame * 200, 0, 50, 60, self.x, self.y)
        pass


def reset_world():
    global running
    global world
    global player

    running = True
    world = []

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
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