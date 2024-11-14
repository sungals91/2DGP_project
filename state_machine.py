

class StateMachine:
    def __init__(self, o):
        self.o = o
        pass

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.o)
        pass

    def update(self):
        self.cur_state.do(self.o)
        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass