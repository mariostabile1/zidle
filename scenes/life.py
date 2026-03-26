import curses
import random

class Scene:
    def __init__(self, stdscr):
        self.grid = []
        self.cols = 0
        self.rows = 0

    def setup(self):
        pass

    def get_delay(self):
        return 0.15

    def _init_grid(self, rows, cols):
        self.grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(1 if random.random() < 0.15 else 0)
            self.grid.append(row)
        self.rows = rows
        self.cols = cols

    def update(self, max_y, max_x):
        # Leave a safe margin for curses terminal edges
        target_rows = max_y - 1
        target_cols = max_x - 1

        if target_rows <= 0 or target_cols <= 0:
            return

        # Re-initialize on resize
        if self.rows != target_rows or self.cols != target_cols:
            self._init_grid(target_rows, target_cols)
            return

        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        alive_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = 0
                # Conway's physics wrap around the screen edges
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr = (r + dr) % self.rows
                        nc = (c + dc) % self.cols
                        neighbors += self.grid[nr][nc]

                if self.grid[r][c] == 1:
                    if neighbors in (2, 3):
                        new_grid[r][c] = 1
                        alive_count += 1
                else:
                    if neighbors == 3:
                        new_grid[r][c] = 1
                        alive_count += 1

        self.grid = new_grid
        
        # Deadlock prevention (reset if heavily dead)
        if alive_count < (self.rows * self.cols) * 0.01:
            self._init_grid(self.rows, self.cols)

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        attr = curses.color_pair(2) if curses.has_colors() else curses.A_NORMAL
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    try:
                        stdscr.addstr(r, c, "█", attr)
                    except curses.error:
                        pass
