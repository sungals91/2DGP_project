from pico2d import load_image, draw_rectangle


class Floor:
    image = None
    def __init__(self):
        self.x, self.y = 400, 200
        if Floor.image == None:
            Floor.image = load_image('image//tile.png')
    def update(self):
        pass
    def draw(self):
        #for i in range(13):
        #    self.image.clip_draw(0,220,70,20,self.x + i*70,self.y)
        self.image.clip_draw(0, 220, 70, 20, self.x, self.y, 600, 20)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 300, self.y - 10, self.x + 300, self.y + 10

    def handle_collision(self, group, other):
        pass