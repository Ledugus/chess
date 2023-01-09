class MainMenu(State):
    pass

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
