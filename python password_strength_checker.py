# 🔐 Password Strength Checker
# Made by me as part of a Cybersecurity & Ethical Hacking project

import tkinter as tk
from tkinter import messagebox
import re
import random
import string

class PasswordStrengthChecker:
    def __init__(self):
        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Password Strength Checker")
        self.window.geometry("600x500")
        self.window.configure(bg="#f0f0f0")

        # Create all the UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.window, text="🔐 Password Strength Checker", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=20)

        # Subtitle
        subtitle = tk.Label(self.window, text="Enter your password below to check its strength", font=("Arial", 12), bg="#f0f0f0", fg="#7f8c8d")
        subtitle.pack()

        # Frame for input field
        input_frame = tk.Frame(self.window, bg="#f0f0f0")
        input_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(input_frame, text="Password:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.password_entry = tk.Entry(input_frame, font=("Arial", 12), width=50, show="*")
        self.password_entry.pack(fill="x", pady=5)

        # Show/hide password
        self.show_password_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility, bg="#f0f0f0").pack(anchor="w")

        # Check button
        tk.Button(self.window, text="Check Password Strength", font=("Arial", 12, "bold"), bg="#3498db", fg="white", command=self.check_password_strength).pack(pady=10)

        # Frame for results
        self.result_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Generate password button
        tk.Button(self.window, text="Generate Strong Password", font=("Arial", 11), bg="#27ae60", fg="white", command=self.generate_strong_password).pack(pady=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def check_password_strength(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to check!")
            return

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        score, feedback, suggestions = self.analyze_password(password)

        if score >= 80:
            strength = "STRONG 💪"
            color = "#27ae60"
        elif score >= 60:
            strength = "MODERATE ⚠️"
            color = "#f39c12"
        else:
            strength = "WEAK ❌"
            color = "#e74c3c"

        # Display results
        tk.Label(self.result_frame, text=f"Password Strength: {strength}", font=("Arial", 16, "bold"), fg=color, bg="#f0f0f0").pack(pady=10)
        tk.Label(self.result_frame, text=f"Score: {score}/100", font=("Arial", 12), bg="#f0f0f0").pack()

        tk.Label(self.result_frame, text="Analysis:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(15, 5), anchor="w")
        for item in feedback:
            tk.Label(self.result_frame, text=f"• {item}", font=("Arial", 10), bg="#f0f0f0", anchor="w", wraplength=500, justify="left").pack(anchor="w", padx=20)

        if suggestions:
            tk.Label(self.result_frame, text="Suggestions:", font=("Arial", 12, "bold"), fg="#e74c3c", bg="#f0f0f0").pack(pady=(15, 5), anchor="w")
            for s in suggestions:
                tk.Label(self.result_frame, text=f"• {s}", font=("Arial", 10), bg="#f0f0f0", anchor="w", wraplength=500, justify="left").pack(anchor="w", padx=20)

    def analyze_password(self, password):
        score = 0
        feedback = []
        suggestions = []

        length = len(password)
        if length >= 12:
            score += 25
            feedback.append(f"✅ Great! Password length is {length} (12+ is best)")
        elif length >= 8:
            score += 15
            feedback.append(f"⚠️ Okay, password has {length} characters")
            suggestions.append("Try to make your password 12+ characters")
        else:
            score += 5
            feedback.append(f"❌ Too short! Only {length} characters")
            suggestions.append("Make your password longer (at least 8 characters)")

        if re.search(r'[a-z]', password):
            score += 10
            feedback.append("✅ Has lowercase letters")
        else:
            suggestions.append("Add some lowercase letters")

        if re.search(r'[A-Z]', password):
            score += 10
            feedback.append("✅ Has uppercase letters")
        else:
            suggestions.append("Add uppercase letters")

        if re.search(r'\d', password):
            score += 10
            feedback.append("✅ Has numbers")
        else:
            suggestions.append("Add numbers (0–9)")

        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', password):
            score += 15
            feedback.append("✅ Has special characters")
        else:
            suggestions.append("Add special characters (!, @, #, etc.)")

        if re.search(r'(.)\1{2,}', password):
            score -= 10
            feedback.append("⚠️ Repeating characters found")
            suggestions.append("Avoid using the same character multiple times")

        common_seqs = ['123', 'abc', 'qwerty', 'asdf']
        if any(seq in password.lower() for seq in common_seqs):
            score -= 15
            feedback.append("⚠️ Common sequence detected")
            suggestions.append("Avoid sequences like '123', 'abc', etc.")

        common_pwds = ['password', '12345678', 'admin', 'welcome']
        if password.lower() in common_pwds:
            score -= 30
            feedback.append("❌ Very common password!")
            suggestions.append("Use something more unique and personal")

        return max(0, score), feedback, suggestions

    def generate_strong_password(self):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-="

        all_chars = lower + upper + digits + symbols
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(symbols)
        ] + [random.choice(all_chars) for _ in range(8)]
        random.shuffle(password)

        generated = ''.join(password)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, generated)
        self.show_password_var.set(True)
        self.password_entry.config(show="")

        messagebox.showinfo("Generated Password", "A strong password has been generated.\nMake sure to save it safely!")
        self.check_password_strength()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordStrengthChecker()
    app.run()
