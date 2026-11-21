from pynput import mouse
import subprocess


def get_active_window_id():
    return subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()


def get_window_pos(win_id):
    output = subprocess.check_output(
        ["xdotool", "getwindowgeometry", "--shell", win_id]
    ).decode()
    geo = dict(line.split("=") for line in output.strip().splitlines() if "=" in line)
    return int(geo["X"]), int(geo["Y"]), int(geo["WIDTH"]), int(geo["HEIGHT"])


# Capture the terminal's window ID right as the script starts
terminal_win_id = get_active_window_id()


def on_move(x, y):
    win_x, win_y, win_w, win_h = get_window_pos(terminal_win_id)

    # Calculate cursor position relative to the terminal's top-left corner
    rel_x = x - win_x
    rel_y = y - win_y

    inside = (0 <= rel_x <= win_w) and (0 <= rel_y <= win_h)
    status = "INSIDE " if inside else "OUTSIDE"

    print(
        f"\r[{status}] Relative: ({rel_x}, {rel_y}) | Global: ({x}, {y})      ",
        end="",
        flush=True,
    )


print("Tracking mouse relative to this terminal... Press Ctrl+C to stop.")
with mouse.Listener(on_move=on_move) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nStopped.")
