import curses
import time
import sys

def run(scene_class):
    try:
        # Wrapper safely establishes alternate screen context and restores it on exit
        curses.wrapper(lambda stdscr: _loop(stdscr, scene_class))
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        # Graceful fallback, ensure terminal settings are restored
        pass

def _loop(stdscr, scene_class):
    try:
        curses.curs_set(0) # Hide cursor
    except curses.error:
        pass
    stdscr.nodelay(1)  # Non-blocking getch
    stdscr.timeout(0)
    stdscr.leaveok(True)
    curses.noecho()
    curses.cbreak()

    # Pre-configure common vibrant colors over default background (-1)
    if curses.has_colors():
        try:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_CYAN, -1)
            curses.init_pair(3, curses.COLOR_RED, -1)
            curses.init_pair(4, curses.COLOR_MAGENTA, -1)
            curses.init_pair(5, curses.COLOR_WHITE, -1)
        except curses.error:
            pass

    scene = scene_class(stdscr)
    scene.setup()

    delay = scene.get_delay()

    while True:
        # Check for user input (exit on any key) -> Getch intrinsically consumes the key
        # leaving our real zsh terminal untouched and free of leaked keystrokes!
        ch = stdscr.getch()
        if ch != -1:
            break

        max_y, max_x = stdscr.getmaxyx()
        
        try:
            scene.update(max_y, max_x)
            scene.render(stdscr, max_y, max_x)
            stdscr.refresh()
        except curses.error:
            # Drop frames cleanly if terminal resizes rapidly
            pass

        time.sleep(delay)
