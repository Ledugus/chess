import pygame as p
from states.state import State
from button import Button
from utils import get_font


class ResultWindow(State):
    def __init__(self, game, winner):
        State.__init__(self, game)
        self.winner = winner
        self.window_width, self.window_height = 400, 400
        self.pos = (
            (self.game.SCREEN_WIDTH - self.window_width) / 2,
            (self.game.SCREEN_HEIGHT - self.window_height) / 2,
        )

        self.window = p.surface.Surface((self.window_width, self.window_height))
        self.window_rect = self.window.get_rect()
        self.new_game_button = Button(
            image=p.image.load("images/play_image.png"),
            pos=(self.pos[0] + self.window_width / 2, self.pos[1] + 150),
            text_input="New Game",
            font=get_font(30),
            height=50,
        )
        self.menu_button = Button(
            image=p.image.load("images/play_image.png"),
            pos=(self.pos[0] + self.window_width / 2, self.pos[1] + 250),
            text_input="Menu",
            font=get_font(30),
            height=50,
        )
        self.close_button = Button(
            image=p.image.load("images/close_button.png"),
            pos=(self.pos[0] + self.window_width - 30, self.pos[1] + 30),
            text_input="",
            font=get_font(20),
            height=20,
        )
        self.window = p.surface.Surface((self.window_width, self.window_height))

    def update(self, actions):
        if actions["left_click"]:
            if self.close_button.check_for_input(actions["mouse_pos"]):
                self.exit_state()
            if self.menu_button.check_for_input(actions["mouse_pos"]):
                self.game.state_stack = self.game.state_stack[:1]
            if self.new_game_button.check_for_input(actions["mouse_pos"]):
                self.game.new_game()

    def render(self, screen):
        self.window.fill(p.Color("white"))
        p.draw.rect(self.window, p.Color("black"), self.window_rect, 3)

        self.game.draw_text(
            self.window,
            self.winner_text(),
            get_font(50),
            p.Color("black"),
            self.window_width / 2,
            50,
        )

        screen.blit(self.window, self.pos)
        self.close_button.render(screen)
        self.menu_button.render(screen)
        self.new_game_button.render(screen)

    def winner_text(self):
        winner_text = ""
        if self.winner[0] == "w":
            winner_text += "White won !"
        elif self.winner[0] == "b":
            winner_text += "Black won !"
        return winner_text

    def how_the_game_ended(self):
        how_the_etc = ""
        if self.winner[1] == "c":
            how_the_etc += "by Checkmate"
        elif self.winner[1] == "r":
            how_the_etc += "by Resign"
        elif self.winner[1] == "s":
            how_the_etc += "by Stalemate"
        return how_the_etc

