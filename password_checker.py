import flet as ft
import re
import random
import string
import math

class PasswordStrengthChecker:
    def __init__(self):
        self.password_input = None
        self.strength_result = None
        self.feedback_column = None
        self.suggestions_column = None
        
    def calculate_strength(self, password):
        if not password:
            return 0, "No password entered"
        
        score = 0
        feedback = []
        suggestions = []
        
        # Length scoring
        if len(password) >= 12:
            score += 25
            feedback.append("✔️ Good length (12+ characters)")
        elif len(password) >= 8:
            score += 15
            feedback.append("✔️ Adequate length (8+ characters)")
        else:
            suggestions.append("💡 Use at least 8 characters")
        
        # Character variety scoring
        if re.search(r'[a-z]', password):
            score += 10
            feedback.append("✔️ Contains lowercase letters")
        else:
            suggestions.append("💡 Add lowercase letters")
            
        if re.search(r'[A-Z]', password):
            score += 10
            feedback.append("✔️ Contains uppercase letters")
        else:
            suggestions.append("💡 Add uppercase letters")
            
        if re.search(r'\d', password):
            score += 10
            feedback.append("✔️ Contains numbers")
        else:
            suggestions.append("💡 Add numbers")
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 15
            feedback.append("✔️ Contains special characters")
        else:
            suggestions.append("💡 Add special characters")
        
        # Complexity bonus
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.7:
            score += 10
            feedback.append("✔️ Good character variety")
        else:
            suggestions.append("💡 Avoid repeated characters")
        
        # Pattern penalties
        if re.search(r'(.)\1{2,}', password):
            score -= 5
            suggestions.append("💡 Avoid repeating characters")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            score -= 5
            suggestions.append("💡 Avoid sequential numbers")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 5
            suggestions.append("💡 Avoid sequential letters")
        
        # Entropy bonus
        if len(password) > 0:
            entropy = len(password) * math.log2(len(set(password)))
            if entropy > 60:
                score += 10
                feedback.append("✔️ High entropy")
        
        score = max(0, min(100, score))
        
        if score >= 80:
            level = "Strong"
        elif score >= 60:
            level = "Medium"
        else:
            level = "Weak"
        
        return score, level, feedback, suggestions
    
    def generate_password(self, length=16):
        characters = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def on_password_change(self, e):
        self.update_strength()
    
    def on_toggle_visibility(self, e):
        self.password_input.password = not self.password_input.password
        self.password_input.suffix = ft.IconButton(
            icon=ft.icons.VISIBILITY if self.password_input.password else ft.icons.VISIBILITY_OFF,
            on_click=self.on_toggle_visibility,
            icon_color=ft.colors.WHITE70
        )
        self.password_input.update()
    
    def on_check_strength(self, e):
        self.update_strength()
    
    def on_generate_password(self, e):
        new_password = self.generate_password()
        self.password_input.value = new_password
        self.password_input.update()
        self.update_strength()
    
    def update_strength(self):
        password = self.password_input.value or ""
        score, level, feedback, suggestions = self.calculate_strength(password)
        
        # Update strength display
        if score >= 80:
            color = ft.colors.GREEN_400
        elif score >= 60:
            color = ft.colors.ORANGE_400
        else:
            color = ft.colors.RED_400
        
        self.strength_result.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Password Strength: {level}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=color
                    ),
                    ft.Container(
                        content=ft.ProgressBar(
                            value=score/100,
                            color=color,
                            bgcolor=ft.colors.WHITE30,
                            height=8
                        ),
                        width=300,
                        border_radius=4
                    ),
                    ft.Text(
                        f"Score: {score}/100",
                        size=16,
                        color=ft.colors.WHITE70
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                border_radius=12,
                border=ft.border.all(1, ft.colors.WHITE30)
            )
        ]
        
        # Update feedback
        feedback_items = []
        for item in feedback:
            feedback_items.append(
                ft.Text(
                    item,
                    size=14,
                    color=ft.colors.GREEN_300,
                    weight=ft.FontWeight.W500
                )
            )
        
        self.feedback_column.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Strengths",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    ),
                    ft.Column(feedback_items) if feedback_items else ft.Text(
                        "No strengths found",
                        size=14,
                        color=ft.colors.WHITE50
                    )
                ]),
                padding=20,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                border_radius=12,
                border=ft.border.all(1, ft.colors.WHITE20)
            )
        ]
        
        # Update suggestions
        suggestion_items = []
        for item in suggestions:
            suggestion_items.append(
                ft.Text(
                    item,
                    size=14,
                    color=ft.colors.ORANGE_300,
                    weight=ft.FontWeight.W500
                )
            )
        
        self.suggestions_column.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Suggestions",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    ),
                    ft.Column(suggestion_items) if suggestion_items else ft.Text(
                        "No suggestions needed",
                        size=14,
                        color=ft.colors.WHITE50
                    )
                ]),
                padding=20,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
                border_radius=12,
                border=ft.border.all(1, ft.colors.WHITE20)
            )
        ]
        
        self.strength_result.update()
        self.feedback_column.update()
        self.suggestions_column.update()

def main(page: ft.Page):
    page.title = "Password Strength Checker"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "SF Pro": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(font_family="SF Pro")
    
    checker = PasswordStrengthChecker()
    
    # Background
    background = ft.Container(
        width=page.window_width or 1200,
        height=page.window_height or 800,
        gradient=ft.LinearGradient(
            colors=[
                "#1e3c72",
                "#2a5298",
                "#4a90e2",
                "#7bb3f0"
            ],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right
        ),
        image_src="https://images.unsplash.com/photo-1519904981063-b0cf448d479e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
        image_fit=ft.ImageFit.COVER,
        image_opacity=0.3
    )
    
    # Password input
    checker.password_input = ft.TextField(
        label="Enter your password",
        password=True,
        width=400,
        height=60,
        text_size=16,
        label_style=ft.TextStyle(color=ft.colors.WHITE70),
        color=ft.colors.WHITE,
        border_color=ft.colors.WHITE30,
        focused_border_color=ft.colors.BLUE_400,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        border_radius=12,
        suffix=ft.IconButton(
            icon=ft.icons.VISIBILITY,
            on_click=checker.on_toggle_visibility,
            icon_color=ft.colors.WHITE70
        ),
        on_change=checker.on_password_change
    )
    
    # Buttons
    check_button = ft.ElevatedButton(
        text="Check Strength",
        on_click=checker.on_check_strength,
        width=180,
        height=50,
        bgcolor=ft.colors.BLUE_600,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=4
        )
    )
    
    generate_button = ft.ElevatedButton(
        text="Generate Password",
        on_click=checker.on_generate_password,
        width=180,
        height=50,
        bgcolor=ft.colors.GREEN_600,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=4
        )
    )
    
    # Results containers
    checker.strength_result = ft.Column([], spacing=10)
    checker.feedback_column = ft.Column([], spacing=10)
    checker.suggestions_column = ft.Column([], spacing=10)
    
    # Main card
    main_card = ft.Container(
        content=ft.Column([
            ft.Text(
                "Password Strength Checker",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=30),
            checker.password_input,
            ft.Container(height=20),
            ft.Row([
                check_button,
                generate_button
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=30),
            checker.strength_result,
            ft.Container(height=20),
            ft.Row([
                ft.Container(
                    content=checker.feedback_column,
                    width=300
                ),
                ft.Container(
                    content=checker.suggestions_column,
                    width=300
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=40,
        bgcolor=ft.colors.with_opacity(0.15, ft.colors.WHITE),
        border_radius=20,
        border=ft.border.all(1, ft.colors.WHITE30),
        shadow=ft.BoxShadow(
            spread_radius=5,
            blur_radius=20,
            color=ft.colors.with_opacity(0.3, ft.colors.BLACK)
        ),
        width=800,
        blur=ft.Blur(20, 20)
    )
    
    # Layout
    page.add(
        ft.Stack([
            background,
            ft.Container(
                content=ft.Column([
                    main_card
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                expand=True
            )
        ])
    )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550)