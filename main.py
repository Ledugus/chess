import pygame as p
import sys
from button import Button
from states.main_menu import MainMenu
from utils import get_font
from utils import is_over


class Game:
    def __init__(self):
        p.init()
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 720
        self.SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.state_stack = []
        self.actions = {"left": False, "right": False, "left_click" : False, "molette_up" : False, "molette_down" : False}
        self.load_states()
    def game_loop(self):
        while self.playing:
            self.get_events()
            self.update()
            self.render()
            
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['up'] = True
                if event.key == pygame.K_s:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True    
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True  

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['up'] = False
                if event.key == pygame.K_s:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False
    def update(self):
        self.state_stack[-1].update(self.actions)
	def load_states(self):
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)
    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        # Render current state to the screen
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()
    
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
    

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
