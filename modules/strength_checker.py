"""
modules/strength_checker.py
Password Strength Checker module for Password Office.
Scores a password based on length, complexity, and character diversity.
Author: Ogbonna Samuel (0xg0fath3r)
"""


def strength_checker_interface():
    """
    Evaluate password strength based on multiple criteria:
    - Length (weak < 8, medium 8-12, strong > 12)
    - Uppercase, lowercase, digits, symbols
    - Bonus for extra length
    Scores and returns WEAK / MEDIUM / STRONG / VERY STRONG.
    """
    print("\n" + "=" * 50)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 50)

    pwd = input("\n[?] Enter password to check: ").strip()

    if not pwd:
        print("[!] No password entered.\n")
        return

    # Analyze composition
    length     = len(pwd)
    has_upper  = any(c.isupper() for c in pwd)
    has_lower  = any(c.islower() for c in pwd)
    has_digit  = any(c.isdigit() for c in pwd)
    has_symbol = any(not c.isalnum() for c in pwd)

    # Scoring system
    score = 0
    if length >= 8:   score += 1
    if length >= 12:  score += 1  # bonus for longer passwords
    if length >= 16:  score += 1  # bonus for very long passwords
    if has_upper:     score += 1
    if has_lower:     score += 1
    if has_digit:     score += 1
    if has_symbol:    score += 1

    # Map score to strength label
    if score <= 2:
        strength = "WEAK"
        icon     = "[✘]"
        tip      = "Add uppercase, digits, and symbols. Use at least 8 characters."
    elif score <= 4:
        strength = "MEDIUM"
        icon     = "[~]"
        tip      = "Good start! Try making it longer and adding more character types."
    elif score <= 6:
        strength = "STRONG"
        icon     = "[✔]"
        tip      = "Great password! Consider going even longer for extra security."
    else:
        strength = "VERY STRONG"
        icon     = "[★]"
        tip      = "Excellent! This is a very secure password."

    # Display results
    print("\n" + "-" * 50)
    print(f"  {icon} Strength : {strength}  (score: {score}/7)")
    print("-" * 50)
    print(f"  Length   : {length} chars    {'✔' if length >= 8 else '✘'}")
    print(f"  Uppercase: {'✔' if has_upper  else '✘'}   Lowercase: {'✔' if has_lower  else '✘'}")
    print(f"  Digits   : {'✔' if has_digit  else '✘'}   Symbols  : {'✔' if has_symbol else '✘'}")
    print("-" * 50)
    print(f"  Tip: {tip}")
    print("-" * 50 + "\n")


def main():
    strength_checker_interface()
