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


def options():

    while True:
        options_mouse_pos = p.mouse.get_pos()

        SCREEN.fill("white")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        SCREEN.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        p.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        mouse_pos = p.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    chess_game()
                if options_button.checkForInput(mouse_pos):
                    options()
                if quit_button.checkForInput(mouse_pos):
                    p.quit()
                    sys.exit()

        p.display.update()

if __name__ == "__main__":
    main_menu()

