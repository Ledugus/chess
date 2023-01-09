import math
import pygame as p
from states.state import State
from chess_engine import GameState, Move
from utils import is_over

class ChessGame(State):  
    def __init__(self, game):
        State.__init__(self, game)
        self.CHESS_BG_COLOR = (178, 190, 191)
        self.BOARD_SIZE = 512
        self.SQ_SIZE = self.BOARD_SIZE / 8
        self.scroll_y = 0
        self.IMAGES = self.load_images()
        self.gs = GameState()
        self.player_clicks = []
        self.sq_selected = ()
        self.valid_moves = []
        self.possible_moves = []
        self.new_selected = False
        p.display.set_caption("Chess Game")
    def load_images(self):
        IMAGES = {}
        pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (self.SQ_SIZE, self.SQ_SIZE))
        return IMAGES

    def update(self, actions):
        if actions["left"]:

            self.gs.undo_move()
            self.new_selected = True
            self.sq_selected = ()

        elif actions["left_click"]:
            self.new_selected = True
            col = actions["mouse_pos"][0] // self.SQ_SIZE
            row = actions["mouse_pos"][1] // self.SQ_SIZE
            if row < 8 and col < 8:
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

        elif actions["molette_up"] and is_over((512, 0, 200, 512), actions["mouse_pos"]):
            self.scroll_y = min(self.scroll_y + 10, 0)
            print(self.scroll_y)
        elif actions["molette_down"] and is_over((512, 0, 200, 512), actions["mouse_pos"]):
            nb_lines = math.ceil(len(self.gs.move_log) / 2)
            taille_move_window = nb_lines * 30
            if taille_move_window < 500:
                self.scroll_y = 0
            else:
                self.scroll_y = max(self.scroll_y - 10, -taille_move_window+500)
            print(self.scroll_y)


        if self.new_selected:
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
        self.board_display()
        self.stats_display()
        self.moves_display()
    def board_display(self):
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(8):
            for c in range(8):
                if (r, c) == self.sq_selected:
                    p.draw.rect(self.game.game_canvas, p.Color("green"), p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                else:
                    color = colors[(r+c)%2]
                    p.draw.rect(self.game.game_canvas, color, p.Rect(c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

                if (r, c) in self.possible_moves:
                    pos = [(c + 0.5) * self.SQ_SIZE, (r + 0.5) * self.SQ_SIZE]
                    if self.gs.board[r][c] == "--":

                        p.draw.circle(self.game.game_canvas, p.Color("green"), pos, 10)
                    else:
                        p.draw.circle(self.game.game_canvas, (0,255, 0, 0.3), pos, (self.SQ_SIZE - 10)/2, 5)
                piece = self.gs.board[r][c]
                if piece != "--":
                    self.game.game_canvas.blit(self.IMAGES[piece],
                                p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
                                )
    def stats_display(self):
        the_font = p.font.Font('freesansbold.ttf', 20)
        text = the_font.render(f'Matériel : ', True, p.Color("black"), p.Color(self.CHESS_BG_COLOR))
        rect = text.get_rect()
        signe = ''
        if self.gs.count_material_delta()>0:
            signe = '+ '
        text1 = the_font.render(signe + str(self.gs.count_material_delta()), True, p.Color("black"))
        self.game.game_canvas.blit(text, (0, self.BOARD_SIZE + 1))
        self.game.game_canvas.blit(text1, (rect.right, self.BOARD_SIZE + 1))
    def moves_display(self):
        move_window = p.surface.Surface((200, 512))
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
            scrollable_moves.blit(text_object, (100*(i%2), (30 * (i//2))+self.scroll_y))

        move_window.blit(title, (4, 4))
        move_window.blit(scrollable_moves, (0, 40))
        p.draw.rect(move_window, p.Color("black"), move_window_rect, 2)
        self.game.game_canvas.blit(move_window, (512, 0))