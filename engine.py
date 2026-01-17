import random

WORDS_DB = [
    "python",
    "terminal",
    "coding",
    "keyboard",
    "algorithm",
    "variable",
    "function",
    "class",
    "monitor",
    "system",
    "linux",
    "interface",
    "gamification",
    "experience",
    "level",
    "stat",
    "wizard",
    "warrior",
    "speed",
    "accuracy",
    "legendary",
    "epic",
    "rare",
    "common",
    "module",
    "structure",
    "design",
    "pattern",
    "loop",
    "string",
    "integer",
    "sudo",
    "./",
    "73951",
    "home",
    "sudo rm -rf /",
    "sudo su",
    "chmod",
    "bash",
    "fish",
    "hyprland",
    "gnome",
    "sudo cp -r ./ /home",
]


class GameEngine:
    def __init__(self, difficulty="normal"):
        self.difficulty = difficulty
        self.word_count = 10 if difficulty == "normal" else 20
        self.target_text = ""

    def generate_text(self):
        self.target_text = " ".join(random.choices(WORDS_DB, k=self.word_count))
        return self.target_text

    def calculate_stats(self, start_time, end_time, typed_text, errors):
        time_taken = end_time - start_time
        minutes = time_taken / 60
        words = len(typed_text) / 5
        wpm = words / minutes if minutes > 0 else 0

        accuracy = 0
        if len(typed_text) > 0:
            accuracy = max(0, (len(typed_text) - errors) / len(typed_text) * 100)

        return wpm, accuracy, time_taken
