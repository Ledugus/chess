import math
import pygame as p
from states.state import State
from states.result_window import ResultWindow
from chess_engine import GameState, Move
from utils import is_over, get_font
from button import Button
class ChessGame(State):  
    def __init__(self, game):
        State.__init__(self, game)
        self.CHESS_BG_COLOR = (178, 190, 191)
        self.BOARD_SIZE = 600
        self.SQ_SIZE = self.BOARD_SIZE / 8
        self.scroll_y = 0
        self.IMAGES = self.load_images()
        self.gs = GameState()
        self.player_clicks = []
        self.sq_selected = ()
        self.valid_moves = []
        self.possible_moves = []
        self.new_selected = False
        self.switch_board_button = Button(image=p.image.load("images/switch.png"), pos=(self.BOARD_SIZE-10, self.BOARD_SIZE+10),
                             text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White", height=20)

        self.resign_button = Button(image=p.image.load("images/play_image.png"), pos=(self.BOARD_SIZE-200, self.BOARD_SIZE+25),
                             text_input="Resign", font=get_font(20), base_color="#d7fcd4", hovering_color="White", height=50)
        self.new_game_button = Button(image=p.image.load("images/play_image.png"), pos=(self.BOARD_SIZE - 200, self.BOARD_SIZE + 25),
                                      text_input="New Game", font=get_font(20), base_color="#d7fcd4", hovering_color="White", height=50)
        self.switched = False
        self.game_ended = False
        self.result_shown = False
        p.display.set_caption("Chess Game")
    def load_images(self):
        images = {}
        pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
        for piece in pieces:
            images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (self.SQ_SIZE, self.SQ_SIZE))
        return images

    def update(self, actions):
        if self.game_ended and not self.result_shown:
            self.result_shown = True
            new_state = ResultWindow(self.game, self.gs.winner)
            new_state.enter_state()
        self.switch_board_button.change_color(actions["mouse_pos"])
        self.resign_button.change_color(actions["mouse_pos"])
        self.new_game_button.change_color(actions["mouse_pos"])
        if actions["left"]:

            self.gs.undo_move()
            self.new_selected = True
            self.sq_selected = ()

        elif actions["left_click"]:
            self.new_selected = True
            if self.switch_board_button.check_for_input(actions["mouse_pos"]):
                self.switched = not self.switched
            if not self.game_ended and self.resign_button.check_for_input(actions["mouse_pos"]):
                self.gs.resign()
            if self.game_ended and self.new_game_button.check_for_input(actions["mouse_pos"]):
                self.game.new_game()

            col = actions["mouse_pos"][0] // self.SQ_SIZE
            row = actions["mouse_pos"][1] // self.SQ_SIZE
            if row < 8 and col < 8:
                if self.switched:
                    row = 7- row
                    col = 7- col
                if self.sq_selected == (row, col):
                    self.sq_selected = ()
                    self.player_clicks = []
                else:
                    self.sq_selected = (round(row), round(col))
                    self.player_clicks.append(self.sq_selected)
                if len(self.player_clicks) == 2:
                    move = Move(self.player_clicks[0], self.player_clicks[1], self.gs.board)
                    if move in self.valid_moves:
                        self.gs.make_move(move)

                        self.gs.checkmate_stalemate()
                        print(move.notation)

                        self.sq_selected = ()
                        self.player_clicks = []
                    else:
                        self.sq_selected = self.player_clicks[1]
                        self.player_clicks = [self.sq_selected]
            else:
                self.sq_selected = ()
                self.player_clicks = []

        elif actions["molette_up"] and is_over((self.BOARD_SIZE, 0, 200, self.BOARD_SIZE), actions["mouse_pos"]):
            self.scroll_y = min(self.scroll_y + 10, 0)
        elif actions["molette_down"] and is_over((self.BOARD_SIZE, 0, 200, self.BOARD_SIZE), actions["mouse_pos"]):
            nb_lines = math.ceil(len(self.gs.move_log) / 2)
            taille_move_window = nb_lines * 30
            if taille_move_window < 500:
                self.scroll_y = 0
            else:
                self.scroll_y = max(self.scroll_y - 10, -taille_move_window+500)


        if not self.game_ended:
            if self.new_selected:
                self.update_possible_moves()
            if self.gs.winner != "":
                self.game_ended = True
    def update_possible_moves(self):

        if self.sq_selected == ():
            self.possible_moves = []
        else:
            self.valid_moves = self.gs.get_valid_moves(self.gs.get_piece_moves(*self.sq_selected))
            self.possible_moves = []

            for move in self.valid_moves:
                self.possible_moves.append((move.end_row, move.end_col))
        self.new_selected = False

    def render(self, screen):
        screen.fill(self.CHESS_BG_COLOR)
        self.board_display(screen)
        self.stats_display(screen)
        self.moves_display(screen)
        self.switch_board_button.update(screen)
        if not self.game_ended:
            self.resign_button.update(screen)
        else:
            self.new_game_button.update(screen)
    def board_display(self,screen):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(8):
            for c in range(8):
                row = r
                col = c
                if self.switched:
                    row = 7 - r
                    col = 7 - c
                if (r, c) == self.sq_selected:
                    p.draw.rect(screen, p.Color("green"), p.Rect(col * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                else:
                    color = colors[(r+c)%2]
                    p.draw.rect(screen, color, p.Rect(col*self.SQ_SIZE, row*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

                if (r, c) in self.possible_moves:
                    pos = [(col + 0.5) * self.SQ_SIZE, (row + 0.5) * self.SQ_SIZE]
                    if self.gs.board[r][c] == "--":

                        p.draw.circle(screen, p.Color("green"), pos, 10)
                    else:
                        p.draw.circle(screen, (0,255, 0), pos, (self.SQ_SIZE - 10)/2, 5)
                piece = self.gs.board[r][c]
                if piece != "--":
                    screen.blit(self.IMAGES[piece],
                                p.Rect(col * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
                                )
    def stats_display(self, screen):
        the_font = p.font.Font('freesansbold.ttf', 20)
        text = the_font.render(f'Matériel : ', True, p.Color("black"), p.Color(self.CHESS_BG_COLOR))
        rect = text.get_rect()
        signe = ''
        if self.gs.count_material_delta()>0:
            signe = '+ '
        text1 = the_font.render(signe + str(self.gs.count_material_delta()), True, p.Color("black"))
        screen.blit(text, (0, self.BOARD_SIZE + 1))
        screen.blit(text1, (rect.right, self.BOARD_SIZE + 1))
    def moves_display(self, screen):
        move_window = p.surface.Surface((200, self.BOARD_SIZE))
        move_window_rect = move_window.get_rect()
        move_window.fill(self.CHESS_BG_COLOR)
        the_font = p.font.Font('freesansbold.ttf', 20)
        title = the_font.render("Moves : ", True, "Black")

        scrollable_moves = p.surface.Surface((200, ((len(self.gs.move_log)//2)+1)*30))
        scrollable_moves.fill(self.CHESS_BG_COLOR)

        for i, move in enumerate(self.gs.move_log):
            text = ''
            checkmate = ''
            if i%2 == 0:
                text = str((i//2)+1) + '. '

            if self.gs.checkmate and i == len(self.gs.move_log)-1:
                checkmate = '#'

            text += move.notation + checkmate
            text_object = the_font.render(text, True, "Black")
            scrollable_moves.blit(text_object, (100*(i%2)+2, (30 * (i//2))+self.scroll_y))

        move_window.blit(title, (4, 4))
        move_window.blit(scrollable_moves, (0, 40))
        p.draw.rect(move_window, p.Color("black"), move_window_rect, 2)
        screen.blit(move_window, (self.BOARD_SIZE, 0))
