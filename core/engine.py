import curses
import time
import sys
import os


def _warn(msg):
    if sys and getattr(sys, "stderr", None):
        # Only print debug diagnostics when explicitly requested
        if os.environ.get("ZIDLE_DEBUG") == "1":
            print(f"[zidle] {msg}", file=sys.stderr)


def run(scene_class):
    try:
        # Wrapper safely establishes alternate screen context and restores it on exit
        curses.wrapper(lambda stdscr: _loop(stdscr, scene_class))
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as exc:
        # Graceful fallback, ensure terminal settings are restored
        _warn(f"engine runtime error: {exc}")


def _swallow_bracketed_paste(stdscr):
    """Consume an in-flight bracketed paste burst.

    getch() just returned ESC (27); ncurses has pushed the unmatched
    sequence tail back to its input FIFO, so the marker continuation
    arrives as ordinary getch() values. If they spell '[200~', read and
    discard the whole paste (up to the closing marker, a size cap, or
    an input gap). Exiting on a paste instead would destroy its opening
    ESC[200~ marker (dropped with the ncurses FIFO at teardown) and hand
    the remainder to the resumed zle prompt as live keystrokes, where
    every newline accepts (executes) a line.
    """
    for expected in b"[200~":
        stdscr.timeout(100)
        ch = stdscr.getch()
        stdscr.timeout(0)
        if ch != expected:
            return False
    stdscr.timeout(100)
    tail = []
    while True:
        ch = stdscr.getch()
        if ch == -1:
            break
        tail.append(ch if 0 <= ch < 256 else 0)
        if bytes(tail[-6:]) == b"\x1b[201~":
            break
        if len(tail) > (1 << 20):
            break
    stdscr.timeout(0)
    curses.flushinp()
    return True


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

    try:
        while True:
            # Check for user input (exit on any key). getch() consumes only the
            # exiting key event; further type-ahead must be discarded explicitly
            # or it survives in the kernel tty queue and reaches the ZLE prompt
            # after we exit.
            ch = stdscr.getch()
            if ch == 27 and _swallow_bracketed_paste(stdscr):
                # Paste fully consumed: keep the screensaver running. A paste
                # must never act as the exit key (see _swallow_bracketed_paste).
                continue
            if ch != -1:
                # Throw away type-ahead not yet read by the program (ncurses
                # FIFO + kernel tty queue). Without this, a leaked newline
                # submits the restored line for execution in the user's shell.
                curses.flushinp()
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
    finally:
        try:
            curses.flushinp()
        except curses.error:
            pass
