import curses
import os
import subprocess
import time

class Scene:
    def __init__(self, stdscr):
        self.cpu = "0%"
        self.ram = "0%"
        self.uptime = "0:00"
        self.last_update = 0

    def setup(self):
        pass

    def get_delay(self):
        return 1.0

    def _get_os_stats(self):
        # Native cross-platform fallback checks. Heavily avoids blocking scripts mapping psutil
        try:
            if os.path.exists("/proc/uptime"):
                with open("/proc/uptime", "r") as f:
                    up_seconds = float(f.readline().split()[0])
                    hours = int(up_seconds // 3600)
                    minutes = int((up_seconds % 3600) // 60)
                    self.uptime = f"{hours}h {minutes}m"
            else:
                out = subprocess.check_output("uptime", shell=True).decode()
                self.uptime = out.split("up ")[1].split(",")[0].strip()
        except:
            self.uptime = "N/A"

        try:
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo", "r") as f:
                    mem = {}
                    for line in f:
                        parts = line.split()
                        mem[parts[0]] = int(parts[1])
                total = mem.get("MemTotal:", 1)
                free = mem.get("MemAvailable:", mem.get("MemFree:", 0))
                self.ram = f"{((total - free) / total * 100):.1f}%"
            else:
                self.ram = "N/A (No /proc)"
        except:
            self.ram = "N/A"

        try:
            if os.path.exists("/proc/loadavg"):
                with open("/proc/loadavg", "r") as f:
                    load = f.readline().split()[0]
                    self.cpu = f"{load} (load sys)"
            else:
                out = subprocess.check_output("uptime", shell=True).decode()
                self.cpu = out.split("load averages: ")[-1].strip() if "load averages:" in out else "N/A"
        except:
            self.cpu = "N/A"

    def update(self, max_y, max_x):
        now = time.time()
        # Cap logic update poll frame at 3 seconds to ensure lightweight IO looping
        if now - self.last_update > 3.0:
            self._get_os_stats()
            self.last_update = now

    def render(self, stdscr, max_y, max_x):
        stdscr.erase()
        color = curses.color_pair(4) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD

        lines = [
            "─── SYSTEM STATS ───",
            "",
            f"CPU Load  : {self.cpu}",
            f"RAM Usage : {self.ram}",
            f"Uptime    : {self.uptime}",
            "",
            "────────────────────"
        ]

        start_y = (max_y - len(lines)) // 2
        for i, line in enumerate(lines):
            start_x = (max_x - len(line)) // 2
            if start_y + i >= 0 and start_y + i < max_y and start_x >= 0 and start_x < max_x:
                try:
                    stdscr.addstr(start_y + i, start_x, line, color)
                except curses.error:
                    pass
