import sys
import tty
import termios
import re


def track_mouse_grid():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    # Regex to parse SGR mouse events: \033[<button;col;rowM (or m for release)
    sgr_pattern = re.compile(r"\033\[<(\d+);(\d+);(\d+)([Mm])")

    try:
        # Switch terminal to raw mode so keypresses and mouse codes arrive immediately
        tty.setraw(fd)

        # ?1003h = Report all mouse movement (even without buttons held)
        # ?1006h = SGR format (supports terminals wider than 223 columns)
        sys.stdout.write("\033[?1003h\033[?1006h")
        sys.stdout.flush()

        sys.stdout.write("Move mouse over terminal (Press 'q' to quit)\r\n")

        while True:
            ch = sys.stdin.read(1)
            if ch == "q" or ch == "\x03":  # 'q' or Ctrl+C
                break

            # Mouse events start with the Escape character (\033)
            if ch == "\033":
                seq = ch
                while True:
                    next_ch = sys.stdin.read(1)
                    seq += next_ch
                    if next_ch in ("M", "m"):
                        break

                match = sgr_pattern.match(seq)
                if match:
                    _, col, row, _ = match.groups()
                    # Terminals use 1-based indexing; subtract 1 if you want 0-based
                    sys.stdout.write(
                        f"\rGrid Position -> Col (X): {col}, Row (Y): {row}   "
                    )
                    sys.stdout.flush()

    finally:
        # Always disable mouse tracking and restore terminal settings on exit!
        sys.stdout.write("\033[?1003l\033[?1006l\r\n")
        sys.stdout.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    track_mouse_grid()
