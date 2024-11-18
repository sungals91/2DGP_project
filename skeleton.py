from pico2d import *
import random
import game_framework
import game_world
from state_machine import *

PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20cm
RUN_SPEED_KMPH = 10.0 # km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

GRAVITY = 10.0 * PIXEL_PER_METER  # 중력 값
JUMP_SPEED = 6.5 * PIXEL_PER_METER


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8 # 애니메이션 마다 다를 수 있음 주의

class Idle:
    @staticmethod
    def enter(skeleton, e):
        print('skeleton Idle Enter')
        pass

    @staticmethod
    def exit(skeleton, e):
        print('skeleton Idle Exit')
        pass

    @staticmethod
    def do(skeleton):
        if skeleton.is_flying:
            skeleton.y -= 1
        skeleton.frame = (skeleton.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(skeleton):
        if skeleton.face_dir == 1:
            skeleton.image.clip_draw(int(skeleton.frame) * 150, 0, 50, 50, skeleton.x, skeleton.y)
        elif skeleton.face_dir == -1:
            skeleton.image.clip_composite_draw(int(skeleton.frame) * 150, 0, 50, 50,
                                          0, 'h', skeleton.x, skeleton.y, 50, 50)

class Walk:
    @staticmethod
    def enter(skeleton, e):
        pass

    @staticmethod
    def exit(skeleton, e):
        pass

    @staticmethod
    def do(skeleton):
        if skeleton.is_flying:
            skeleton.jump_speed -= GRAVITY * game_framework.frame_time
            skeleton.y += skeleton.jump_speed * game_framework.frame_time
        skeleton.x += skeleton.dir * RUN_SPEED_PPS * game_framework.frame_time
        skeleton.frame = (skeleton.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if skeleton.x > 600:
            skeleton.dir = -1
        elif skeleton.x < 200:
            skeleton.dir = 1
        skeleton.x = clamp(200, skeleton.x, 600)
        pass

    @staticmethod
    def draw(skeleton):
        if skeleton.face_dir == 1:
            skeleton.image.clip_draw(int(skeleton.frame) * 150, 75 * 2, 50, 50, skeleton.x, skeleton.y)
        elif skeleton.face_dir == -1:
            skeleton.image.clip_composite_draw(int(skeleton.frame) * 150, 72 * 2, 50, 50,
                                          0, 'h', skeleton.x, skeleton.y, 50, 50)
        pass

class Hit:
    @staticmethod
    def enter():
        pass

class Skeleton:
    image = None
    def __init__(self):
        if Skeleton.image == None:
            Skeleton.image = load_image('image\\skeleton.png')
        self.x, self.y = 600, 300
        self.dir = random.choice([-1, 1])
        self.jump_speed = 0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Walk)
        self.state_machine.set_transitions(
            {
                Idle: {},
                Walk: {}
            }
        )
        self.is_flying = True
        self.face_dir = 1
        self.hp = 1

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 15, self.y + 25
        pass

    def handle_collision(self, group, other):
        if group == 'enemy:floor':
            print('FLOOR COLLISION')
            self.is_flying = False
        if group == 'player_atk:skeleton_hit' and other.collide_state == 'atk':
            print('SKELETON HIT')
            self.hp -= 1
            if self.hp == 0:
                game_world.remove_object(self)
        pass