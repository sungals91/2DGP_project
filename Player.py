from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDL_KEYUP


class Player:
    def __init__(self):
        self.image = load_image('image\\player.png')
        self.x, self.y = 400, 300
        self.dir_x, self.dir_y = 0,0
        self.frame = 0
        pass
    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir_x * 5
        self.y += self.dir_y * 5
    pass
    def draw(self):
        self.image.clip_draw(self.frame * 200, 0, 50, 60, self.x, self.y)
        pass

    def handle_event(self, event):

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir_x += 1
            elif event.key == SDLK_LEFT:
                self.dir_x -= 1
            elif event.key == SDLK_UP:
                self.dir_y += 1
            elif event.key == SDLK_DOWN:
                self.dir_y -= 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir_x -= 1
            elif event.key == SDLK_LEFT:
                self.dir_x += 1
            elif event.key == SDLK_UP:
                self.dir_y -= 1
            elif event.key == SDLK_DOWN:
                self.dir_y += 1
