import random
import curses

class Scene:
    def __init__(self, stdscr):
        self.drops = []
        self.chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
        
    def setup(self):
        pass

    def get_delay(self):
        return 0.05

    def update(self, max_y, max_x):
        # Add new vertical "streams"
        while len(self.drops) < max_x // 3:
            x = random.randint(0, max_x - 1)
            y = random.randint(-max_y, 0)
            length = random.randint(5, max(5, max_y - 2))
            speed = random.randint(1, 2)
            self.drops.append({"x": x, "y": y, "len": length, "speed": speed})

        # Progress elements downward
        for drop in self.drops:
            drop["y"] += drop["speed"]

        # Evict old drops from memory
        self.drops = [d for d in self.drops if d["y"] - d["len"] < max_y]

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        for drop in self.drops:
            x = drop["x"]
            head_y = drop["y"]
            
            for i in range(drop["len"]):
                y = head_y - i
                if 0 <= y < max_y and 0 <= x < max_x:
                    char = random.choice(self.chars)
                    # Pull green from the preset engine pairs natively
                    color = curses.color_pair(1) if curses.has_colors() else 0
                    
                    if i == 0:
                        try: # High-intensity white/bold head
                            stdscr.addstr(y, x, char, color | curses.A_BOLD)
                        except curses.error: pass
                    else:
                        try: # Dimmer green tail
                            stdscr.addstr(y, x, char, color)
                        except curses.error: pass
