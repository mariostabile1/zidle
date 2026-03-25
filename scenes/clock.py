import time
import curses

class Scene:
    def __init__(self, stdscr):
        self.digits = {
            '0': ["███", "█ █", "█ █", "█ █", "███"],
            '1': ["  █", "  █", "  █", "  █", "  █"],
            '2': ["███", "  █", "███", "█  ", "███"],
            '3': ["███", "  █", "███", "  █", "███"],
            '4': ["█ █", "█ █", "███", "  █", "  █"],
            '5': ["███", "█  ", "███", "  █", "███"],
            '6': ["███", "█  ", "███", "█ █", "███"],
            '7': ["███", "  █", "  █", "  █", "  █"],
            '8': ["███", "█ █", "███", "█ █", "███"],
            '9': ["███", "█ █", "███", "  █", "███"],
            ':': ["   ", " █ ", "   ", " █ ", "   "]
        }
        self.flash = True

    def setup(self):
        pass

    def get_delay(self):
        return 0.5

    def update(self, max_y, max_x):
        self.flash = not self.flash

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        current_time = time.strftime("%H:%M:%S")
        if not self.flash:
            current_time = current_time.replace(":", " ")

        color = curses.color_pair(2) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD

        # Width calculation is chars horizontally * padding
        total_width = len(current_time) * 4 - 1
        start_x = (max_x - total_width) // 2
        start_y = (max_y - 5) // 2

        if start_x < 0 or start_y < 0:
            return

        for row in range(5):
            x_offset = start_x
            for char in current_time:
                art = self.digits.get(char, ["   "] * 5)
                try:
                    stdscr.addstr(start_y + row, x_offset, art[row], color)
                except curses.error:
                    pass
                x_offset += 4
