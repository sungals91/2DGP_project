from pico2d import load_image, draw_rectangle, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDL_KEYUP

import game_framework
from state_machine import *

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20cm
RUN_SPEED_KMPH = 20.0 # km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

GRAVITY = 10.0 * PIXEL_PER_METER  # 중력 값
JUMP_SPEED = 6.5 * PIXEL_PER_METER

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
            player.jump_speed -= GRAVITY * game_framework.frame_time
            player.y += player.jump_speed * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 200, 0, 50, 50, player.x, player.y)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 200, 0, 50, 50,
                                          0, 'h', player.x, player.y, 50, 50)

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
            player.jump_speed -= GRAVITY * game_framework.frame_time
            player.y += player.jump_speed * game_framework.frame_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 200, 75 * 6, 50, 50, player.x, player.y)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 200, 75 * 6, 50, 50,
                                          0, 'h', player.x, player.y, 50, 50)

class Jump:
    @staticmethod
    def enter(player, e):
        print('Player Jump Enter')
        player.is_flying = True  # 점프 중 상태
        player.jump_speed = JUMP_SPEED
        player.start_y = player.y
        pass

    @staticmethod
    def exit(player, e):
        print('Player Jump Exit')
        player.jump_speed = 0
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 2 * ACTION_PER_TIME * game_framework.frame_time) % 2
        player.jump_speed -= GRAVITY * game_framework.frame_time
        player.y += player.jump_speed * game_framework.frame_time
        if player.jump_speed <= 0:
            player.is_flying = True
            if player.y - player.start_y <= 0:
                player.state_machine.add_event(('LAND', 0))
        print(f'{player.is_flying}')

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 200, 75 * 5, 50, 50, player.x, player.y)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 200, 75 * 5, 50, 50,
                                             0, 'h', player.x, player.y, 50, 50)

class Attack:
    @staticmethod
    def enter(player, e):
        player.collide_state = 'atk'
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 6 * ACTION_PER_TIME * game_framework.frame_time) % 6
        if int(player.frame) == 5:
            player.collide_state = 'idle'
            player.state_machine.add_event(('ACT_END', 0))
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 200, 75 * 1, 125, 75, player.x + (125/2) - 25, player.y + (75/2)-25)
        elif player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 200, 75 * 1, 125, 75,
                                          0, 'h', player.x - (125/2) + 25, player.y + (75/2)-25, 125, 75)
        pass



class Player:
    def __init__(self):
        self.image = load_image('image\\player.png')
        self.x, self.y = 400, 300
        self.dir_x, self.dir_y = 0,0
        self.jump_speed = 0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, up_down : Jump, a_down : Attack},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Jump, a_down : Attack},
                Jump: {land : Idle, a_down : Attack},
                Attack: {act_end : Idle},
            }
        )
        self.is_flying = True
        self.face_dir = 1
        self.collide_state = 'idle'
        self.hp = 1
        self.exp = 0

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def get_bb(self):
        if self.collide_state == 'idle':
            return self.x -25, self.y - 25, self.x + 25, self.y + 25
        elif self.collide_state == 'atk':
            if self.face_dir == 1:
                return self.x -25, self.y - 25, self.x + 75, self.y + 25
            elif self.face_dir == -1:
                return self.x -75, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:floor':
            print('FLOOR COLLISION')
            self.is_flying = False
        elif group == 'player_atk:skeleton_hit':
            if self.collide_state == 'atk':
                self.exp += 10
            elif self.collide_state == 'idle':
                self.hp -= 1
                print(f'{self.hp}')
        pass