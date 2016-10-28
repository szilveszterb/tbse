from g2048.ai import *
from multiprocessing import Process

class aiPlay:
    def __init__(self,game,interval=1000,ai=AI()):
        self.ai=ai
        self.game=game
        self.interval=interval

    def move(self):
        direction = self.ai.actuate(self.game)
        if direction is not None:
            self.game.shift(direction)
