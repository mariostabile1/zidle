import curses
import random

class Scene:
    def __init__(self, stdscr):
        self.text = " ZIDLE "
        self.x = 10
        self.y = 5
        self.dx = 2
        self.dy = 1
        self.color = 1

    def setup(self):
        pass

    def get_delay(self):
        return 0.1

    def update(self, max_y, max_x):
        self.x += self.dx
        self.y += self.dy
        
        hit = False
        width = len(self.text)

        # Bounce Vertical
        if self.y <= 0:
            self.y = 0
            self.dy = 1
            hit = True
        elif self.y >= max_y - 1:
            self.y = max(0, max_y - 2)
            self.dy = -1
            hit = True

        # Bounce Horizontal
        if self.x <= 0:
            self.x = 0
            self.dx = 2
            hit = True
        elif self.x >= max_x - width:
            self.x = max(0, max_x - width - 1)
            self.dx = -2
            hit = True

        if hit:
            self.color = random.randint(1, 5)

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        attr = curses.color_pair(self.color) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        
        if 0 <= self.y < max_y and 0 <= self.x < max_x - len(self.text):
            try:
                stdscr.addstr(int(self.y), int(self.x), self.text, attr)
            except curses.error:
                pass
