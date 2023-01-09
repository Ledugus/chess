from button import Button
from states.state import State
import pygame as p
from utils import get_font
from states.chess_game import ChessGame
class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.BG = p.transform.scale(p.image.load('images/wp2883270.jpg'), (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        self.play_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.quit_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    def update(self, actions):
        if actions["left_click"] and self.play_button.check_for_input(actions["mouse_pos"]):
            new_state = ChessGame(self.game)
            new_state.enter_state()


    def render(self, display):

            
        display.blit(self.BG, (0, 0))

        mouse_pos = p.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        display.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.change_color(mouse_pos)
            button.update(display)