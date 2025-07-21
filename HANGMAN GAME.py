import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json

# ---------------------- CONFIGURATION ----------------------
WORDS = ["python", "guitar", "hangman", "wizard", "rocket"]
MAX_ATTEMPTS = 6
SCORE_FILE = "hangman_score.json"

# ---------------------- HANGMAN GAME ----------------------
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 Hangman Game")
        self.root.geometry("600x600")
        self.root.configure(bg="#1e1e1e")

        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.attempts = 0
        self.score = 0
        self.high_score = self.load_high_score()

        self.build_gui()
        self.update_display()

    def build_gui(self):
        self.title_label = tk.Label(self.root, text="HANGMAN GAME", font=("Consolas", 26, "bold"), fg="white", bg="#1e1e1e")
        self.title_label.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Courier", 22), fg="white", bg="#1e1e1e")
        self.word_label.pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.buttons_frame.pack()
        self.letter_buttons = {}

        for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=ch, width=4, font=("Arial", 12, "bold"), bg="#333", fg="white",
                            activebackground="#555", command=lambda c=ch: self.make_guess(c.lower()))
            btn.grid(row=i // 9, column=i % 9, padx=3, pady=3)
            self.letter_buttons[ch] = btn

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {MAX_ATTEMPTS}", font=("Arial", 14), fg="tomato", bg="#1e1e1e")
        self.attempts_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score} | High Score: {self.high_score}", font=("Arial", 13), fg="lightgreen", bg="#1e1e1e")
        self.score_label.pack(pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"), fg="yellow", bg="#1e1e1e")
        self.result_label.pack(pady=10)

        self.hint_button = tk.Button(self.root, text="💡 Hint", command=self.show_hint, font=("Arial", 12), bg="#008cba", fg="white")
        self.hint_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="🔁 Play Again", command=self.reset_game, state="disabled")
        self.reset_button.pack(pady=10)

    def update_display(self):
        display = " ".join([ch if ch in self.guessed_letters else "_" for ch in self.word])
        self.word_label.config(text=display.upper())
        self.attempts_label.config(text=f"Attempts left: {MAX_ATTEMPTS - self.attempts}")
        self.score_label.config(text=f"Score: {self.score} | High Score: {self.high_score}")

        if "_" not in display:
            self.score += 5
            self.result_label.config(text="🎉 You Win!", fg="lightgreen")
            self.check_high_score()
            self.end_game()

    def make_guess(self, letter):
        self.letter_buttons[letter.upper()].config(state="disabled")
        if letter in self.word:
            self.guessed_letters.add(letter)
        else:
            self.attempts += 1
            self.score -= 2

        if self.attempts >= MAX_ATTEMPTS:
            self.word_label.config(text=" ".join(self.word.upper()))
            self.result_label.config(text="💀 You Lost!", fg="red")
            self.end_game()
        else:
            self.update_display()

    def show_hint(self):
        hidden_letters = [ch for ch in self.word if ch not in self.guessed_letters]
        if hidden_letters:
            hint_letter = random.choice(hidden_letters)
            self.guessed_letters.add(hint_letter)
            self.letter_buttons[hint_letter.upper()].config(state="disabled")
            self.score -= 3
            self.update_display()

    def check_high_score(self):
        if self.score > self.high_score:
            name = simpledialog.askstring("New High Score!", "Enter your name:")
            if name:
                self.high_score = self.score
                self.save_high_score(name, self.score)

    def load_high_score(self):
        try:
            with open(SCORE_FILE, "r") as file:
                data = json.load(file)
                return data.get("score", 0)
        except:
            return 0

    def save_high_score(self, name, score):
        with open(SCORE_FILE, "w") as file:
            json.dump({"name": name, "score": score}, file)

    def end_game(self):
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")
        self.hint_button.config(state="disabled")
        self.reset_button.config(state="normal")

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.attempts = 0
        self.result_label.config(text="")
        self.reset_button.config(state="disabled")
        self.hint_button.config(state="normal")

        for btn in self.letter_buttons.values():
            btn.config(state="normal")

        self.update_display()

# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
