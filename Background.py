from pico2d import load_image


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
