import pygame as p
from utils import get_font
from button import Button
from states.state import State
from states.chess_game import ChessGame
class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.BG = p.transform.scale(p.image.load('images/wp2883270.jpg'), (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        self.buttons = [Button(image=p.image.load("images/play_image.png"), pos=(game.SCREEN_WIDTH/2, 250),
                             text_input="PLAY", font=get_font(75), height=150),
                        Button(image=p.image.load("images/play_image.png"), pos=(game.SCREEN_WIDTH/2, 550),
                             text_input="QUIT", font=get_font(75), height=150)
                        ]
    def update(self, actions):
        for button in self.buttons:
            button.change_color(actions["mouse_pos"])
        if actions["left_click"] and self.buttons[0].check_for_input(actions["mouse_pos"]):
            new_state = ChessGame(self.game)
            new_state.enter_state()
    def render(self, display):
        display.blit(self.BG, (0, 0))

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(self.game.SCREEN_WIDTH/2, 100))

        display.blit(menu_text, menu_rect)

        for button in self.buttons:
            button.update(display)