from button import Button

class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.BG = None
        self.play_button = Button(image=p.image.load("images/play_image.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.play_button_rect = self.play_button.get_rect()
        self.quit_button = Button(image=p.image.load("images/play_image.png"), pos=(game.mid_, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        self.quit_button_rect = self.play
    def update(self, actions):
        if actions["left_click"] and is_over(actions["mouse_pos"]):
            new_state = ChessGame(self.game)
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "Game States Demo", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )
            
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
