from utils import get_font
from utils import is_over
import pygame as p
import sys
from button import Button
import chess_engine



class Game:
    def __init__(self):
        p.init()
p.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
CHESS_BG_COLOR = (178, 190, 191)
SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG = p.transform.scale(p.image.load('images/wp2883270.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}

p.display.set_caption("Menu")

def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def chess_game():
    scroll_y = 0
    p.display.set_caption("CHESS : New Game")
    clock = p.time.Clock()
    SCREEN.fill(CHESS_BG_COLOR)
    gs = chess_engine.GameState()
    possible_moves = []
    valid_moves = []
    new_selected = False
    load_images()
    running = True
    sq_selected = () # (row, col)
    player_clicks = [] # list of squares
    while running:
        location = p.mouse.get_pos()

        for e in p.event.get():

            if e.type == p.QUIT:
                p.quit()
                exit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    new_selected = True
                    sq_selected = ()

            elif e.type == p.MOUSEBUTTONDOWN and e.button == 4 and is_over((512, 0, 200, 512), location):
                scroll_y = min(scroll_y + 10, 0)
                print(scroll_y)
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 5 and is_over((512, 0, 200, 512), location):
                scroll_y = max(scroll_y - 10, (-((len(gs.move_log) // 2) + 1) * 30)+500)
                print(scroll_y)
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                new_selected = True
                col =  location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if row < 8 and col < 8:
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (round(row), round(col))
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        if move in valid_moves:
                            gs.make_move(move)
                            gs.checkmate_stalemate()
                            print(move.notation)
                            sq_selected = ()
                            player_clicks = []
                        else:
                            sq_selected = player_clicks[1]
                            player_clicks = [sq_selected]
                else:
                    sq_selected = ()
                    player_clicks = []


        if new_selected:
            if sq_selected == ():
                possible_moves = []
            else:
                valid_moves = gs.get_valid_moves(gs.get_piece_moves(*sq_selected))
                possible_moves = []

                for move in valid_moves:
                    possible_moves.append((move.end_row, move.end_col))
            new_selected = False
        draw_game_state(SCREEN, gs, sq_selected, possible_moves, scroll_y)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs, sq_selected, possible_moves, scroll_y):
    screen.fill(CHESS_BG_COLOR)
    draw_board(screen, sq_selected, possible_moves, gs)
    draw_pieces(screen, gs.board)
    draw_stats(screen, gs)
    show_moves(screen, gs, scroll_y)
def draw_board(screen, sq_selected, possible_moves, gs):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (r, c) == sq_selected:
                p.draw.rect(screen, p.Color("green"), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                color = colors[(r+c)%2]
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            if (r, c) in possible_moves:
                pos = [(c + 0.5) * SQ_SIZE, (r + 0.5) * SQ_SIZE]
                if gs.board[r][c] == "--":

                    p.draw.circle(screen, p.Color("green"), pos, 10)
                else:
                    p.draw.circle(screen, (0,255, 0, 0.3), pos, (SQ_SIZE - 10)/2, 5)
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def draw_stats(screen, gs):
    the_font = p.font.Font('freesansbold.ttf', 20)
    text = the_font.render(f'Matériel : ', True, p.Color("black"), p.Color(CHESS_BG_COLOR))
    rect = text.get_rect()
    signe = ''
    message = ''
    if gs.count_material_delta()>0:
        signe = '+ '
    text1 = the_font.render(signe + str(gs.count_material_delta()), True, p.Color("black"))
    screen.blit(text, (0, BOARD_HEIGHT + 1))
    screen.blit(text1, (rect.right, BOARD_HEIGHT + 1))
    if gs.checkmate:
        message = "Checkmate !"
    if gs.stalemate:
        message = "Stalemate !"
    if message != '':
        text2 = the_font.render(message, True, p.Color("black"))
        screen.blit(text2, (0, SCREEN_HEIGHT - 100))
def show_moves(screen , gs, scroll_y):

    move_window = p.surface.Surface((200, 512))
    move_window_rect = move_window.get_rect()
    move_window.fill(CHESS_BG_COLOR)
    the_font = p.font.Font('freesansbold.ttf', 20)
    title = the_font.render("Moves : ", True, "Black")

    scrollable_moves = p.surface.Surface((200, ((len(gs.move_log)//2)+1)*30))
    scrollable_moves.fill(CHESS_BG_COLOR)

    for i, move in enumerate(gs.move_log):
        text = ''
        checkmate = ''
        if i%2 == 0:
            text = str((i//2)+1) + '. '

        if gs.checkmate and i == len(gs.move_log)-1:
            checkmate = '#'

        text += move.notation + checkmate
        text_object = the_font.render(text, True, "Black")
        scrollable_moves.blit(text_object, (100*(i%2), (30 * (i//2))+scroll_y))

    move_window.blit(title, (4, 4))
    move_window.blit(scrollable_moves, (0, 40))
    p.draw.rect(move_window, p.Color("black"), move_window_rect, 2)
    screen.blit(move_window, (512, 0))

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

