import curses


def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.addstr(0, 0, "Click anywhere in the terminal (Press 'q' to quit)")

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            stdscr.addstr(
                2, 0, f"Clicked terminal cell -> Col (X): {x}, Row (Y): {y}   "
            )
            stdscr.refresh()


curses.wrapper(main)
