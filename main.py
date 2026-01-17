import curses

from ui import GameUI


def main(stdscr):
    # Ukryj kursor
    curses.curs_set(0)
    ui = GameUI(stdscr)
    ui.main_loop()


if __name__ == "__main__":
    curses.wrapper(main)
