"""
modules/manager.py
Encrypted Password Manager module for Password Office.
Uses Fernet symmetric encryption to store passwords securely in JSON.
File paths are configurable via .env for portability and security.
Author: Ogbonna Samuel (0xg0fath3r)
"""

import os
import json
from getpass import getpass
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env file in project root
load_dotenv()

# Paths loaded from .env — falls back to safe defaults
BASE     = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE, os.getenv("DATA_DIR", "data"))
KEY_FILE = os.path.join(BASE, os.getenv("KEY_FILE", "data/key.key"))
DB_FILE  = os.path.join(BASE, os.getenv("DB_FILE",  "data/passwords.enc"))


# ── Data directory & key management ───────────────────────────────────────────

def ensure_data():
    """Create data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_or_create_key():
    """
    Load an existing Fernet key from KEY_FILE, or generate and save a new one.
    Returns: bytes key
    """
    ensure_data()
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("[+] New encryption key created.\n")
        return key
    with open(KEY_FILE, "rb") as f:
        return f.read()


# ── Encryption helpers ─────────────────────────────────────────────────────────

def save_list(lst, fernet):
    """Encrypt and save the password list to DB_FILE."""
    raw   = json.dumps(lst).encode("utf-8")
    token = fernet.encrypt(raw)
    with open(DB_FILE, "wb") as f:
        f.write(token)


def load_list(fernet):
    """
    Decrypt and load the password list from DB_FILE.
    Returns empty list if file doesn't exist.
    Returns None if decryption fails (wrong key or corrupted).
    """
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "rb") as f:
        blob = f.read()
    try:
        raw = fernet.decrypt(blob)
    except Exception:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


# ── CRUD operations ────────────────────────────────────────────────────────────

def add_password(fernet):
    """Prompt and save a new password entry."""
    print("\n" + "=" * 50)
    print("          ADD NEW PASSWORD")
    print("=" * 50)

    label    = input("\n[?] Label (e.g., Gmail, Facebook): ").strip()
    username = input("[?] Username / email              : ").strip()
    password = getpass("[?] Password (input hidden)       : ").strip()

    if not label or not username or not password:
        print("[!] All fields are required. Aborting.\n")
        return

    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database. Try resetting the DB.\n")
        return

    # Check for duplicate label
    existing = [e for e in lst if e.get("label", "").lower() == label.lower()]
    if existing:
        overwrite = input(f"[!] '{label}' already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("[*] Cancelled.\n")
            return
        lst = [e for e in lst if e.get("label", "").lower() != label.lower()]

    lst.append({"label": label, "username": username, "password": password})
    save_list(lst, fernet)
    print(f"[+] '{label}' saved successfully.\n")


def view_labels(fernet):
    """Display all saved labels and usernames (no passwords shown)."""
    print("\n" + "=" * 50)
    print("          SAVED PASSWORDS")
    print("=" * 50)

    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database. Try resetting the DB.\n")
        return
    if not lst:
        print("[!] No saved passwords yet.\n")
        return

    print()
    for i, e in enumerate(lst, start=1):
        print(f"  [{i}] {e.get('label', '<no-label>'):<20} {e.get('username', '')}")
    print()


def show_details(fernet):
    """Reveal full details including password for a selected entry."""
    print("\n" + "=" * 50)
    print("        SHOW PASSWORD DETAILS")
    print("=" * 50)

    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database. Try resetting the DB.\n")
        return
    if not lst:
        print("[!] No saved passwords yet.\n")
        return

    print()
    for i, e in enumerate(lst, start=1):
        print(f"  [{i}] {e.get('label', '<no-label>')}")

    choice = input("\n[?] Enter number to reveal (or Enter to cancel): ").strip()
    if not choice:
        print("[*] Cancelled.\n")
        return
    if not choice.isdigit():
        print("[!] Invalid input.\n")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(lst):
        print("[!] Number out of range.\n")
        return

    entry = lst[idx]
    print("\n" + "-" * 50)
    print(f"  Label   : {entry.get('label')}")
    print(f"  Username: {entry.get('username')}")
    print(f"  Password: {entry.get('password')}")
    print("-" * 50 + "\n")


def delete_one(fernet):
    """Delete a single password entry by number."""
    print("\n" + "=" * 50)
    print("         DELETE ONE PASSWORD")
    print("=" * 50)

    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database. Try resetting the DB.\n")
        return
    if not lst:
        print("[!] No saved passwords yet.\n")
        return

    print()
    for i, e in enumerate(lst, start=1):
        print(f"  [{i}] {e.get('label', '<no-label>')}")

    choice = input("\n[?] Enter number to delete (or Enter to cancel): ").strip()
    if not choice:
        print("[*] Cancelled.\n")
        return
    if not choice.isdigit():
        print("[!] Invalid input.\n")
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(lst):
        print("[!] Number out of range.\n")
        return

    label   = lst[idx].get("label", "this entry")
    confirm = input(f"[?] Delete '{label}'? (y/N): ").strip().lower()
    if confirm != "y":
        print("[*] Cancelled.\n")
        return

    del lst[idx]
    save_list(lst, fernet)
    print(f"[+] '{label}' deleted.\n")


def delete_all(fernet):
    """Wipe the entire encrypted database."""
    print("\n" + "=" * 50)
    print("         DELETE ALL PASSWORDS")
    print("=" * 50)

    confirm = input("\n[?] Type DELETE to confirm wiping all saved passwords: ").strip()
    if confirm != "DELETE":
        print("[*] Cancelled.\n")
        return
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print("[+] All passwords deleted.\n")


def reset_database():
    """Wipe both key and database files for a full reset."""
    print("\n" + "=" * 50)
    print("       RESET DATABASE (FULL WIPE)")
    print("=" * 50)
    print("\n[!] WARNING: This will permanently delete your key and all passwords!")

    confirm = input("[?] Type RESET to confirm: ").strip()
    if confirm != "RESET":
        print("[*] Cancelled.\n")
        return
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
    print("[+] Database and key removed. A new key will be created on next use.\n")


# ── Main interface ─────────────────────────────────────────────────────────────

def manager_interface():
    """Interactive password manager CLI."""
    ensure_data()
    key    = load_or_create_key()
    fernet = Fernet(key)

    while True:
        print("\n" + "=" * 50)
        print("          PASSWORD MANAGER")
        print("=" * 50)
        print("""
  [1] Add new password
  [2] View saved labels
  [3] Show password details
  [4] Delete one password
  [5] Delete ALL passwords
  [6] Reset database (wipe key + DB)
  [7] Return to main menu
""")
        choice = input("  Choose (1-7): ").strip()

        if   choice == "1": add_password(fernet)
        elif choice == "2": view_labels(fernet)
        elif choice == "3": show_details(fernet)
        elif choice == "4": delete_one(fernet)
        elif choice == "5": delete_all(fernet)
        elif choice == "6": reset_database()
        elif choice == "7":
            print("[*] Returning to main menu.\n")
            break
        else:
            print("[!] Invalid option. Please choose 1-7.\n")


def main():
    manager_interface()
