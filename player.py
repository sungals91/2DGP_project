from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDL_KEYUP
from state_machine import *

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20cm
RUN_SPEED_KMPH = 20.0 # km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Idle:
    @staticmethod
    def enter(player):
        print('Player Idle Enter')
        pass

    @staticmethod
    def exit(player):
        print('Player Idle Exit')
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 200, 0, 50, 60, player.x, player.y)

class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass


class Player:
    def __init__(self):
        self.image = load_image('image\\player.png')
        self.x, self.y = 400, 300
        self.dir_x, self.dir_y = 0,0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def update(self):
        #self.frame = (self.frame + 1) % 8
        #self.x += self.dir_x * 5
        #self.y += self.dir_y * 5
        self.state_machine.update()

    def draw(self):
        #self.image.clip_draw(self.frame * 200, 0, 50, 60, self.x, self.y)
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass