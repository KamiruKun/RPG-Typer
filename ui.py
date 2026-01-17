import curses
import time

from engine import GameEngine
from player import THEMES, Player


class GameUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.player = Player()
        curses.start_color()
        curses.use_default_colors()
        self.apply_theme()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Error
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # UI
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight

        self.engine = GameEngine()

    def apply_theme(self):
        theme_name = self.player.active_theme
        fg, bg = THEMES.get(theme_name, THEMES["Default"])
        curses.init_pair(1, fg, bg)

    def draw_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        title = f"=== TERMINAL RPG TYPER - Poziom {self.player.level} ==="
        subtitle = f"Best WPM: {self.player.best_wpm:.1f}"

        self.stdscr.addstr(
            h // 2 - 5,
            (w - len(title)) // 2,
            title,
            curses.color_pair(3) | curses.A_BOLD,
        )
        self.stdscr.addstr(
            h // 2 - 3, (w - len(subtitle)) // 2, subtitle, curses.color_pair(4)
        )

        options = [
            "[ ENTER ] Start game",
            "[ T ] Change theme",
            "[ I ] Player stats",
            "[ S ] Settings",
            "[ Q ] Quit",
        ]
        for idx, option in enumerate(options):
            self.stdscr.addstr(h // 2 + idx, (w - len(option)) // 2, option)

        self.stdscr.refresh()

    def show_themes_menu(self):
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            self.stdscr.addstr(2, (w - 14) // 2, "--- THEMES ---", curses.color_pair(3))

            for i, theme in enumerate(self.player.unlocked_themes):
                prefix = "[X]" if theme == self.player.active_theme else "[ ]"
                text = f"{i + 1}. {prefix} {theme}"
                self.stdscr.addstr(4 + i, (w - len(text)) // 2, text)

            self.stdscr.addstr(h - 2, (w - 25) // 2, "Press B to go back")
            self.stdscr.refresh()

            try:
                key = self.stdscr.getkey()
            except:
                continue

            if key.lower() == "b":
                break

            if len(key) == 1 and key.isdigit():
                idx = int(key) - 1
                if 0 <= idx < len(self.player.unlocked_themes):
                    self.player.active_theme = self.player.unlocked_themes[idx]
                    self.apply_theme()
                    self.player.save_data()

    def show_stats_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        lines = [
            "--- Player Stats ---",
            f"Level: {self.player.level}",
            f"XP: {self.player.xp} / {self.player.xp_to_next}",
            f"Gold: {self.player.gold}",
            "",
            f"Best WPM: {self.player.best_wpm:.2f}",
            f"Total rounds: {self.player.total_rounds}",
            f"Rounds won: {self.player.rounds_won}",
            "",
            "Press any key to back...",
        ]

        for i, line in enumerate(lines):
            color = curses.color_pair(4) if "---" in line else curses.color_pair(0)
            self.stdscr.addstr(h // 2 - 5 + i, (w - len(line)) // 2, line, color)

        self.stdscr.getch()

    def show_settings_screen(self):
        """Nowe menu ustawień"""
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()

            title = "--- SETTINGS ---"
            self.stdscr.addstr(
                h // 2 - 5, (w - len(title)) // 2, title, curses.color_pair(3)
            )

            opt_diff = f"[ 1 ] Difficulty: {self.engine.difficulty.upper()}"
            opt_words = f"[ 2 ] Words per round: {self.engine.word_count}"
            opt_back = "[ B ] Back to Menu"

            self.stdscr.addstr(h // 2 - 2, (w - len(opt_diff)) // 2, opt_diff)
            self.stdscr.addstr(h // 2 - 1, (w - len(opt_words)) // 2, opt_words)
            self.stdscr.addstr(h // 2 + 2, (w - len(opt_back)) // 2, opt_back)

            self.stdscr.refresh()

            try:
                key = self.stdscr.getkey()
            except:
                continue

            if key == "1":
                if self.engine.difficulty == "normal":
                    self.engine.difficulty = "hard"
                else:
                    self.engine.difficulty = "normal"

            elif key == "2":
                counts = [10, 20, 30, 50]
                try:
                    current_idx = counts.index(self.engine.word_count)
                    new_idx = (current_idx + 1) % len(counts)
                    self.engine.word_count = counts[new_idx]
                except ValueError:
                    self.engine.word_count = 10

            elif key.lower() == "b":
                break

    def run_game_loop(self):
        target_text = self.engine.generate_text()
        current_text = []
        start_time = None
        errors = 0
        combo = 0
        max_combo = 0

        curses.flushinp()

        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()

            self.stdscr.addstr(2, 2, "Type:", curses.A_BOLD)

            for i, char in enumerate(target_text):
                color = curses.color_pair(0)
                if i < len(current_text):
                    if current_text[i] == char:
                        color = curses.color_pair(1)
                    else:
                        color = curses.color_pair(2)
                elif i == len(current_text):
                    color = curses.color_pair(4) | curses.A_REVERSE

                self.stdscr.addch(4, 2 + i, char, color)

            if start_time:
                elapsed = time.time() - start_time
                wpm_live = (
                    (len(current_text) / 5) / (elapsed / 60) if elapsed > 0 else 0
                )
                stats = f"Time: {elapsed:.1f}s | WPM: {wpm_live:.1f} | Combo: {combo}x"
                self.stdscr.addstr(h - 2, 2, stats, curses.color_pair(3))
            else:
                self.stdscr.addstr(h - 2, 2, "Start typing...", curses.color_pair(3))

            self.stdscr.refresh()

            if len(current_text) == len(target_text):
                end_time = time.time()
                return self.engine.calculate_stats(
                    start_time, end_time, "".join(current_text), errors
                ), max_combo

            try:
                key = self.stdscr.getkey()
            except:
                continue

            if not start_time:
                start_time = time.time()

            if key in ("KEY_BACKSPACE", "\b", "\x7f"):
                if len(current_text) > 0:
                    current_text.pop()

            elif len(key) == 1 and ord(key) == 27:  # ESC
                return None, 0

            elif len(key) == 1:
                if len(current_text) < len(target_text):
                    current_text.append(key)
                    expected_char = target_text[len(current_text) - 1]
                    if key == expected_char:
                        combo += 1
                        if combo > max_combo:
                            max_combo = combo
                    else:
                        errors += 1
                        combo = 0

    def show_results(self, stats, max_combo):
        wpm, accuracy, time_taken = stats

        base_xp = int(wpm)
        accuracy_bonus = int(accuracy * 0.5)
        combo_bonus = max_combo * 2
        total_xp = base_xp + accuracy_bonus + combo_bonus

        leveled_up = self.player.gain_xp(total_xp)
        self.player.total_rounds += 1
        if wpm > self.player.best_wpm:
            self.player.best_wpm = wpm

        gold_gained = int(total_xp / 10)
        self.player.gold += gold_gained

        self.player.save_data()

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        lines = [
            f"Round info",
            f"----------------",
            f"WPM: {wpm:.2f}",
            f"Accuracy: {accuracy:.1f}%",
            f"Max Combo: {max_combo}",
            f"",
            f"EXP gained: {total_xp}",
            f"Gold gained: {gold_gained}",
            f"Level progress: {self.player.xp} / {self.player.xp_to_next}",
            f"",
            "!!! LEVEL UP !!!" if leveled_up else "",
            f"",
            "Press any key...",
        ]

        for i, line in enumerate(lines):
            color = curses.color_pair(1) if "LEVEL UP" in line else curses.color_pair(0)
            self.stdscr.addstr(h // 2 - 6 + i, (w - len(line)) // 2, line, color)

        self.stdscr.getch()

    def main_loop(self):
        while True:
            self.draw_menu()
            try:
                key = self.stdscr.getkey()
            except:
                continue

            if key == "\n":
                result, max_combo = self.run_game_loop()
                if result:
                    self.show_results(result, max_combo)

            elif key.lower() == "t":
                self.show_themes_menu()

            elif key.lower() == "i":
                self.show_stats_screen()

            elif key.lower() == "s":
                self.show_settings_screen()

            elif key.lower() == "q":
                break
