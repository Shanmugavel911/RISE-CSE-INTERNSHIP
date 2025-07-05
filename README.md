# Password Strength Checker

A modern, immersive password strength checker built with Flet in Python. Features a beautiful glass-like interface with real-time password analysis.

## Features

- **Modern Glass UI**: Transparent, rounded glass-like interface with blur effects
- **Beautiful Background**: Fullscreen gradient background with optional image overlay
- **Real-time Analysis**: Instant password strength checking as you type
- **Comprehensive Scoring**: Evaluates length, character variety, patterns, and entropy
- **Visual Feedback**: Color-coded strength indicator (Green/Orange/Red)
- **Password Generator**: Generate secure random passwords
- **Detailed Feedback**: Shows both strengths and improvement suggestions
- **Password Visibility Toggle**: Show/hide password with eye icon
- **Responsive Design**: Centered layout that works on different screen sizes
- **Web-based**: Runs in your browser to avoid desktop dependencies

## Installation

1. Install Python 3.8 or higher
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python password_checker.py
```

The app will open in your default web browser at `http://localhost:8550`

## Password Scoring

The application evaluates passwords based on:
- **Length**: 8+ characters (adequate), 12+ characters (good)
- **Character Types**: Lowercase, uppercase, numbers, special characters
- **Complexity**: Character variety and uniqueness
- **Patterns**: Penalizes repetitive and sequential patterns
- **Entropy**: Rewards high information entropy

**Scoring Levels:**
- **Strong**: 80-100 points (Green)
- **Medium**: 60-79 points (Orange)  
- **Weak**: 0-59 points (Red)

## Controls

- **Password Input**: Type your password to check
- **Eye Icon**: Toggle password visibility
- **Check Strength**: Manual strength check (also checks automatically)
- **Generate Password**: Create a secure random password

The app provides real-time feedback showing what makes your password strong and suggestions for improvement.
