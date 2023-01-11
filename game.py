import pygame as p
from states.main_menu import MainMenu
from states.main_menu import ChessGame
class Game:
    def __init__(self):
        p.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 720
        self.game_canvas = p.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.state_stack = []
        self.actions = {"left": False, "right": False, "left_click" : False, "molette_up" : False, "molette_down" : False}
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)
    def game_loop(self):
        while self.playing:
            self.get_events()
            self.update()
            self.render()
            self.reset_keys()
            
    def get_events(self):
        self.actions["mouse_pos"] = p.mouse.get_pos()
        for event in p.event.get():
            if event.type == p.QUIT:
                self.playing = False
                self.running = False
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions["left_click"] = True
                if event.button == 4:
                    self.actions["molette_up"] = True
                if event.button == 5:
                    self.actions["molette_down"] = True
            if event.type == p.MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions["left_click"] = False

            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == p.K_LEFT:
                    self.actions['left'] = True
                if event.key == p.K_RIGHT:
                    self.actions['right'] = True

            if event.type == p.KEYUP:
                if event.key == p.K_LEFT:
                    self.actions['left'] = False

        return self.actions
    def update(self):
        self.state_stack[-1].update(self.actions)
    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        p.display.flip()
    def new_game(self):
        self.state_stack = [MainMenu(self)]
        new_game_obj = ChessGame(self)
        new_game_obj.enter_state()
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
    @staticmethod
    def draw_text(surface, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        # text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
