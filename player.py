from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDL_KEYUP

import game_framework
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
    def enter(player, e):
        print('Player Idle Enter')
        pass

    @staticmethod
    def exit(player, e):
        print('Player Idle Exit')
        pass

    @staticmethod
    def do(player):
        if player.is_flying:
            player.y -= 1
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 200, 0, 50, 60, player.x, player.y)


class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir  = -1, -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if player.is_flying:
            player.y -= 1
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 200, 75 * 6, 50, 50, player.x, player.y)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 200, 75 * 6, 50, 50,
                                          0, 'h', player.x, player.y, 50, 50)
        pass


class Player:
    def __init__(self):
        self.image = load_image('image\\player.png')
        self.x, self.y = 400, 300
        self.dir_x, self.dir_y = 0,0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            }
        )
        self.is_flying = True

    def update(self):
        #self.frame = (self.frame + 1) % 8
        #self.x += self.dir_x * 5
        #self.y += self.dir_y * 5
        self.state_machine.update()

    def draw(self):
        #self.image.clip_draw(self.frame * 200, 0, 50, 60, self.x, self.y)
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def get_bb(self):
        return self.x -25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:floor':
            print('FLOOR COLLISION')
            self.is_flying = False
        pass