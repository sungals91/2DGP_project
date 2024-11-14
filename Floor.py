from pico2d import load_image


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
