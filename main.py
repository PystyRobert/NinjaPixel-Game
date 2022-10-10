from game import Game

g = Game()

while g.run:
    g.curr_menu.display_menu()
    if g.play:
        g.show_start_screen()
        g.wait_for_key()
        g.game_loop()
        if g.lost:
            g.show_defeat_screen()
            g.wait_for_key()
