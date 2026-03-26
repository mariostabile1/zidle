import random
import curses

class Scene:
    def __init__(self, stdscr):
        self.stars = []
        self.max_stars = 120
        
    def setup(self):
        pass

    def get_delay(self):
        return 0.05

    def update(self, max_y, max_x):
        cx = max_x / 2
        cy = max_y / 2
        
        # Add new stars originating from the center
        while len(self.stars) < self.max_stars:
            # Subtle random offset from direct center
            x = cx + random.uniform(-2, 2)
            y = cy + random.uniform(-1, 1)
            
            # Vectors pointing away from center
            dx = (x - cx) * 0.1
            dy = (y - cy) * 0.1
            
            # Give a push to perfectly centered stagnant stars
            if abs(dx) < 0.01 and abs(dy) < 0.01:
                dx = random.choice([-0.2, 0.2])
                dy = random.choice([-0.1, 0.1])
            
            self.stars.append({"x": x, "y": y, "dx": dx, "dy": dy, "age": 0})

        # Move strings and simulate z-axis acceleration
        for star in self.stars:
            star["x"] += star["dx"]
            star["y"] += star["dy"]
            star["dx"] *= 1.12
            star["dy"] *= 1.12
            star["age"] += 1

        # Culling
        self.stars = [s for s in self.stars if 0 <= s["x"] < max_x and 0 <= s["y"] < max_y]

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        for star in self.stars:
            x, y = int(star["x"]), int(star["y"])
            if 0 <= y < max_y and 0 <= x < max_x:
                char = '.'
                if star["age"] > 12: char = '+'
                if star["age"] > 22: char = '*'
                if star["age"] > 30: char = '●'
                    
                color = curses.color_pair(5) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
                try:
                    stdscr.addstr(y, x, char, color)
                except curses.error:
                    pass
