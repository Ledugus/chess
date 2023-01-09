from utils import get_font
from utils import is_over
import pygame as p
import sys
from button import Button
import chess_engine



class Game:
    def __init__(self):
        p.init()
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 720
        self.SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running, self.playing = True
        self.state_stack =[]
    BG = p.transform.scale(p.image.load('images/wp2883270.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    

if __name__ == "__main__":
    main_menu()

