# Password Checker - Simple App made by me
# Checks how strong a password is and gives suggestions

import tkinter as tk
from tkinter import messagebox
import re
import random
import string

class PasswordApp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Password Checker")
        self.win.geometry("600x500")
        self.win.configure(bg="#eaeaea")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.win, text="Password Strength Checker", font=("Arial", 18, "bold"), bg="#eaeaea").pack(pady=20)
        tk.Label(self.win, text="Enter a password to test", font=("Arial", 11), bg="#eaeaea").pack()

        input_box = tk.Frame(self.win, bg="#eaeaea")
        input_box.pack(pady=15)

        tk.Label(input_box, text="Password:", font=("Arial", 11), bg="#eaeaea").pack(anchor="w")
        self.entry = tk.Entry(input_box, font=("Arial", 11), width=40, show="*")
        self.entry.pack(pady=5)

        self.show_pw = tk.BooleanVar()
        tk.Checkbutton(input_box, text="Show", variable=self.show_pw, command=self.toggle_pw, bg="#eaeaea").pack(anchor="w")

        tk.Button(self.win, text="Check", font=("Arial", 11), bg="#007acc", fg="white", command=self.check_pw).pack(pady=10)
        tk.Button(self.win, text="Generate Strong Password", font=("Arial", 10), bg="#2e8b57", fg="white", command=self.make_password).pack()

        self.output = tk.Frame(self.win, bg="#eaeaea")
        self.output.pack(pady=15)

    def toggle_pw(self):
        self.entry.config(show="" if self.show_pw.get() else "*")

    def check_pw(self):
        pwd = self.entry.get()
        if not pwd:
            messagebox.showwarning("Empty", "Enter something first.")
            return

        for w in self.output.winfo_children():
            w.destroy()

        score, pros, cons = self.evaluate(pwd)

        if score >= 80:
            msg = "Strong"
            color = "green"
        elif score >= 60:
            msg = "Okay"
            color = "orange"
        else:
            msg = "Weak"
            color = "red"

        tk.Label(self.output, text=f"Result: {msg}", font=("Arial", 13, "bold"), fg=color, bg="#eaeaea").pack()
        tk.Label(self.output, text=f"Score: {score}/100", font=("Arial", 11), bg="#eaeaea").pack()

        if pros:
            tk.Label(self.output, text="Good:", font=("Arial", 11, "bold"), bg="#eaeaea").pack(anchor="w")
            for i in pros:
                tk.Label(self.output, text=f"- {i}", font=("Arial", 10), bg="#eaeaea").pack(anchor="w", padx=20)

        if cons:
            tk.Label(self.output, text="Suggestions:", font=("Arial", 11, "bold"), fg="red", bg="#eaeaea").pack(anchor="w", pady=(10, 0))
            for i in cons:
                tk.Label(self.output, text=f"- {i}", font=("Arial", 10), bg="#eaeaea").pack(anchor="w", padx=20)

    def evaluate(self, p):
        s = 0
        good = []
        bad = []

        if len(p) >= 12:
            s += 25
            good.append("Good length.")
        elif len(p) >= 8:
            s += 15
            bad.append("Try 12+ chars.")
        else:
            s += 5
            bad.append("Too short.")

        if re.search(r'[a-z]', p): s += 10; good.append("Has lowercase.")
        else: bad.append("Add lowercase letters.")

        if re.search(r'[A-Z]', p): s += 10; good.append("Has uppercase.")
        else: bad.append("Add uppercase letters.")

        if re.search(r'\d', p): s += 10; good.append("Has numbers.")
        else: bad.append("Add some digits.")

        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', p): s += 15; good.append("Has symbols.")
        else: bad.append("Add special characters.")

        if re.search(r'(.)\1{2,}', p):
            s -= 10
            bad.append("Too many repeats.")

        common = ['123', 'abc', 'qwerty', 'password']
        for c in common:
            if c in p.lower():
                s -= 15
                bad.append("Avoid common patterns.")
                break

        return max(s, 0), good, bad

    def make_password(self):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        nums = string.digits
        symbols = "!@#$%^&*()_+-="
        all_set = lower + upper + nums + symbols

        pwd = [
            random.choice(lower),
            random.choice(upper),
            random.choice(nums),
            random.choice(symbols)
        ] + [random.choice(all_set) for _ in range(8)]

        random.shuffle(pwd)
        new_pwd = ''.join(pwd)

        self.entry.delete(0, tk.END)
        self.entry.insert(0, new_pwd)
        self.show_pw.set(True)
        self.entry.config(show="")
        self.check_pw()

    def run(self):
        self.win.mainloop()

if __name__ == "__main__":
    app = PasswordApp()
    app.run()
