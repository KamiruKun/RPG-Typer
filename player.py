import curses
import json
import os

SAVE_FILE = "player_data.json"

THEMES = {
    "Default": (curses.COLOR_GREEN, curses.COLOR_BLACK),
    "Magenta": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    "Cyan": (curses.COLOR_CYAN, curses.COLOR_BLACK),
    "Lava": (curses.COLOR_RED, curses.COLOR_BLACK),
    "Midnight": (curses.COLOR_BLUE, curses.COLOR_BLACK),
    "Gold": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
    "Forest": (curses.COLOR_GREEN, curses.COLOR_WHITE),
}


class Player:
    def __init__(self):
        self.name = "Gracz"
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.total_rounds = 0
        self.rounds_won = 0
        self.unlocked_themes = ["Default"]
        self.active_theme = "Default"
        self.best_wpm = 0
        self.gold = 0
        self.load_data()

    def gain_xp(self, amount):
        self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            if self.level == 2:
                self.unlocked_themes.append("Magenta")
            if self.level == 4:
                self.unlocked_themes.append("Midnight")
            if self.level == 6:
                self.unlocked_themes.append("Cyan")
            if self.level == 8:
                self.unlocked_themes.append("Forest")
            if self.level == 10:
                self.unlocked_themes.append("Lava")
            if self.level == 12:
                self.unlocked_themes.append("Gold")
            self.xp_to_next = int(self.xp_to_next * 1.2)
            leveled_up = True
        return leveled_up

    def save_data(self):
        data = {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "total_rounds": self.total_rounds,
            "rounds_won": self.rounds_won,
            "unlocked_themes": self.unlocked_themes,
            "active_theme": self.active_theme,
            "best_wpm": self.best_wpm,
            "gold": self.gold,
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.name = data.get("name", "Gracz")
                self.level = data.get("level", 1)
                self.xp = data.get("xp", 0)
                self.xp_to_next = data.get("xp_to_next", 100)
                self.total_rounds = data.get("total_rounds", 0)
                self.rounds_won = data.get("rounds_won", 0)
                self.unlocked_themes = data.get("unlocked_themes", ["Default"])
                self.active_theme = data.get("active_theme", "Default")
                self.best_wpm = data.get("best_wpm", 0)
                self.gold = data.get("gold", 0)
