from pico2d import *
import random
import game_framework
from state_machine import *

PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20cm
RUN_SPEED_KMPH = 20.0 # km / Hour
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
        skeleton.frame = (skeleton.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(skeleton):
        if skeleton.face_dir == 1:
            skeleton.image.clip_draw(int(skeleton.frame) * 150, 0, 50, 50, skeleton.x, skeleton.y)
        elif skeleton.face_dir == -1:
            skeleton.image.clip_composite_draw(int(skeleton.frame) * 150, 0, 50, 50,
                                          0, 'h', skeleton.x, skeleton.y, 50, 50)

class Skeleton:
    image = None
    def __init__(self):
        if Skeleton.image == None:
            Skeleton.image = load_image('image\\skeleton.png')
        self.x, self.y = 400, 300
        self.dir_x, self.dir_y = 0, 0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {},
            }
        )
        self.is_flying = True
        self.face_dir = 1

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass