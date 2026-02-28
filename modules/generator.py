"""
modules/generator.py
Password Generator module for Password Office.
Generates a cryptographically random password of user-specified length.
Author: Ogbonna Samuel (0xg0fath3r)
"""

import random
import string


def generator_interface():
    """
    Interactive password generator.
    Prompts user for length and character set preferences,
    then generates and displays a strong random password.
    """
    print("\n" + "=" * 50)
    print("         PASSWORD GENERATOR")
    print("=" * 50)

    # Prompt for password length
    try:
        length = int(input("\n[?] Enter password length (min 4): ").strip())
    except ValueError:
        print("[!] Invalid input. Please enter a number.\n")
        return

    if length < 4:
        print("[!] Length too short. Minimum is 4 characters.\n")
        return

    # Ask user what character sets to include
    print("\n[?] Include character types (press Enter to skip):")
    use_upper   = input("    Uppercase letters? (Y/n): ").strip().lower() != "n"
    use_lower   = input("    Lowercase letters? (Y/n): ").strip().lower() != "n"
    use_digits  = input("    Digits?            (Y/n): ").strip().lower() != "n"
    use_symbols = input("    Symbols?           (Y/n): ").strip().lower() != "n"

    # Build character pool
    chars = ""
    if use_upper:   chars += string.ascii_uppercase
    if use_lower:   chars += string.ascii_lowercase
    if use_digits:  chars += string.digits
    if use_symbols: chars += string.punctuation

    # Fallback if user excluded everything
    if not chars:
        print("[!] No character types selected. Using all characters by default.\n")
        chars = string.ascii_letters + string.digits + string.punctuation

    # Generate password
    password = "".join(random.choice(chars) for _ in range(length))

    # Display result
    print("\n" + "-" * 50)
    print(f"[+] Generated Password ({length} chars):\n")
    print(f"    {password}")
    print("-" * 50 + "\n")


def main():
    generator_interface()
