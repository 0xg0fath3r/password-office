#!/usr/bin/env python3   #(This helps executes the codes by just calling the file name in Kali Linux)
# Standard library imports
import os
import sys
import time
import random
from colorama import init, Fore, Style
 
# Initialize colorama for cross-platform terminal coloring
init(autoreset=True)
 
# I Imported modules from modules/
import modules.manager
import modules.strength_checker
import modules.generator
import modules.policy_checker


 
BANNER = r"""
 ██▓███   ▄▄▄        ██████   ██████  █     █░ ▒█████   ██▀███  ▓█████▄ 
▓██░  ██▒▒████▄    ▒██    ▒ ▒██    ▒ ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌
▓██░ ██▓▒▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒░██   █▌
▒██▄█▓▒ ▒░██▄▄▄▄██   ▒   ██▒  ▒   ██▒░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ░▓█▄   ▌
▒██▒ ░  ░ ▓█   ▓██▒▒██████▒▒▒██████▒▒░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒░▒████▓ 
▒▓▒░ ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒▓  ▒ 
░▒ ░       ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░  ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ▒  ▒ 
░░         ░   ▒   ░  ░  ░  ░░  ░  ░    ░   ░  ░ ░ ░ ▒    ░░   ░  ░ ░  ░ 
               ░  ░      ░        ░      ░        ░ ░     ░        ░    
                                                                 ░       
 
 ▒█████    █████▒ █████▒██▓ ▄████▄  ▓█████                              
▒██▒  ██▒▓██   ▒▓██   ▒▓██▒▒██▀ ▀█  ▓█   ▀                              
▒██░  ██▒▒████ ░▒████ ░▒██▒▒▓█    ▄ ▒███                                
▒██   ██░░▓█▒  ░░▓█▒  ░░██░▒▓▓▄ ▄██▒▒▓█  ▄                              
░ ████▓▒░░▒█░   ░▒█░   ░██░▒ ▓███▀ ░░▒████▒                             
░ ▒░▒░▒░  ▒ ░    ▒ ░   ░▓  ░ ░▒ ▒  ░░░ ▒░ ░                             
  ░ ▒ ▒░  ░      ░      ▒ ░  ░  ▒    ░ ░  ░                             
░ ░ ░ ▒   ░ ░    ░ ░    ▒ ░░           ░                                
    ░ ░                 ░  ░ ░         ░  ░                             
                           ░                                            
"""


# Gradient colors (H2 palette)
GRADIENT_COLORS = [Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

# SIMPLE UTILITY
def clear_screen():
    """Clear terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text: str, delay: float = 0.002):
    """
    Print text with a typing animation.
    - text: string to print
    - delay: seconds delay between characters
    """
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(text: str = "Loading", duration: float = 1.6):
    """
    Simple spinner for short loading effect.
    - text: message shown next to spinner
    - duration: how many seconds spinner runs
    """
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        for f in frames:
            sys.stdout.write(f"\r{Fore.YELLOW}{text} {f}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.08)
    print()

# Method to create random security qoutes
def random_quote() -> str:
    """This function return a decorative cybersecurity quote."""
    quotes = [
        "“Security is a process, not a product.” — Bruce Schneier",
        "“In cybersecurity, there is no finish line.”",
        "“The quieter you become, the more you are able to hear.” — Kali",
        "“Trust, but verify.” — Ronald Reagan",
    ]
    return random.choice(quotes)


# BANNER PRINTING Method
def print_gradient_banner(banner: str, colors: list):
    """
    Apply a single smooth gradient across the entire banner string.
    - We build a color map for each character position and apply it deterministically.
    - Using splitlines(keepends=True) preserves newline characters so mapping matches positions.
    """
    # Flatten banner characters and compute total length including newlines
    full_text = banner
    total = len(full_text)
    if total == 0:
        return

    # Precompute color selection for each character index
    color_map = []
    color_count = len(colors)
    for i in range(total):
        ratio = i / max(1, total - 1)  # 0..1
        scaled = ratio * (color_count - 1)  # 0..color_count-1
        # Choose nearest color index for smooth block transitions
        idx = int(round(scaled))
        color_map.append(colors[idx])

    # Now print line by line using the mapping. Use splitlines(True) to keep newline chars.
    pos = 0
    for line in banner.splitlines(True):  # keeps newline chars
        line_builder = []
        for ch in line:
            # apply color for this char
            col = color_map[pos] if pos < len(color_map) else Style.RESET_ALL
            # append colored character; color reset after each char to prevent leaking
            line_builder.append(col + ch + Style.RESET_ALL)
            pos += 1
        # join and print the colored line
        sys.stdout.write("".join(line_builder))
    # ensure final newline
    print()
    

# Show_banner Method
def show_banner():
    """
    Display the full intro:
    - Clear screen
    - Print gradient banner
    - Print title, creator, version with typing animation
    - Spinner and random quote
    """
    clear_screen()
    print_gradient_banner(BANNER, GRADIENT_COLORS)
    print(Fore.WHITE + "=" * 80)
    slow_print(Fore.GREEN + "PASSWORD OFFICE — Secure Password Suite".center(80), delay=0.0015)
    slow_print(Fore.CYAN + "Created by: Ogbonna Samuel".center(80), delay=0.0015)
    slow_print(Fore.MAGENTA + "Version 1.0  —  2025".center(80), delay=0.0015)
    print(Fore.WHITE + "=" * 80)
    spinner("Initializing System")
    slow_print(Fore.GREEN + random_quote().center(80), delay=0.0015)
    print(Fore.WHITE + "=" * 80 + "\n")


# Main menu Method
def main_menu():
    """
    Main interactive loop presenting the five options.
    - Exit option printed in red.
    - Delegates to simple modules.
    """
    while True:
        # Menu options 
        print(Fore.CYAN + "[1] Password Generator")
        print(Fore.CYAN + "[2] Password Strength Checker")
        print(Fore.CYAN + "[3] Password Policy Checker")
        print(Fore.CYAN + "[4] Password Manager")
        # Exit in RED to stand out
        print(Fore.RED + "[5] Exit Application" + Style.RESET_ALL)
        print()  # spacing

        choice = input(Fore.YELLOW + "Select an option (1-5): " + Style.RESET_ALL).strip()

        # Dispatch to module functions 
        if choice == "1":
            modules.generator.main()
        elif choice == "2":
            modules.strength_checker.check_strength()
        elif choice == "3":
            modules.policy_checker.main()
        elif choice == "4":
            modules.manager.main()
        elif choice == "5":
            # Clean exit message and break the loop
            print(Fore.GREEN + "\nThank you for using PASSWORD OFFICE — Stay secure!\n" + Style.RESET_ALL)
            break
        else:
            # Friendly error on invalid input; 
            print(Fore.RED + "[!] Invalid option. Please choose 1-5.\n" + Style.RESET_ALL)


# Start App Method
def main():
    """
    Program entrypoint:
    - show_banner: display intro + animations
    - main_menu: start the interactive UI
    """
    show_banner()
    main_menu()

if __name__ == "__main__":
    main()
