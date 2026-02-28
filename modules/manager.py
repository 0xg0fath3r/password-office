"""
modules/manager.py
Very simple encrypted password manager using Fernet (cryptography).
- Stores a list of entries in JSON, encrypted as one blob.
- Minimal feature set (presentation-friendly):
    * Add password
    * View labels
    * Show details (reveal)
    * Delete one
    * Delete all
    * Reset database (delete key + file)
    * Return to main menu
- Code intentionally small and commented for explanation.
"""

import os
import json
from getpass import getpass
from cryptography.fernet import Fernet

# Paths relative to project root
BASE = os.path.dirname(os.path.dirname(__file__))  # project root
DATA_DIR = os.path.join(BASE, "data")
KEY_FILE = os.path.join(DATA_DIR, "key.key")
DB_FILE = os.path.join(DATA_DIR, "passwords.enc")


# Ensure data dir, key management

def ensure_data():
    """Create data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_or_create_key():
    """
    Load an existing Fernet key from KEY_FILE, or create and save a new one.
    Returns: bytes key
    """
    ensure_data()
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Encryption 
def save_list(lst, fernet):
    """
    Save Python list as JSON and encrypt the bytes to DB_FILE.
    Overwrites previous DB_FILE.
    """
    raw = json.dumps(lst).encode("utf-8")
    token = fernet.encrypt(raw)
    with open(DB_FILE, "wb") as f:
        f.write(token)

def load_list(fernet):
    """
    Load and decrypt DB_FILE. Returns list (empty if not present).
    If decryption fails, return None to indicate problem.
    """
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "rb") as f:
        blob = f.read()
    try:
        raw = fernet.decrypt(blob)
    except Exception:
        # Wrong key or corrupted file
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None

# Add Password Method

def add_password(fernet):
    """Prompt and add a new password entry."""
    print("\n=== ADD NEW PASSWORD ===")
    label = input("Label (e.g., Gmail, Facebook): ").strip()
    username = input("Username / email: ").strip()
    password = getpass("Password (input hidden): ").strip()
    if not label or not username or not password:
        print("[!] All fields required. Aborting.\n")
        return
    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database (wrong key or corrupted). Choose Reset DB.\n"); return
    entry = {"label": label, "username": username, "password": password}
    lst.append(entry)
    save_list(lst, fernet)
    print("[+] Saved entry.\n")
# Method to view labels
def view_labels(fernet):
    """Show numbered list of saved labels (no passwords displayed)."""
    print("\n=== SAVED PASSWORDS ===")
    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database (wrong key or corrupted). Choose Reset DB.\n"); return
    if not lst:
        print("[!] No saved passwords.\n"); return
    for i, e in enumerate(lst, start=1):
        print(f"[{i}] {e.get('label','<no-label>')}  —  {e.get('username','')}")
    print()

# Show details method
def show_details(fernet):
    """Reveal full details (including password) for one selected entry."""
    print("\n=== SHOW PASSWORD DETAILS ===")
    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database (wrong key or corrupted). Choose Reset DB.\n"); return
    if not lst:
        print("[!] No saved passwords.\n"); return
    for i, e in enumerate(lst, start=1):
        print(f"[{i}] {e.get('label','<no-label>')}")
    choice = input("\nEnter number to reveal (or press Enter to cancel): ").strip()
    if not choice:
        print("[*] Cancelled.\n"); return
    if not choice.isdigit():
        print("[!] Invalid.\n"); return
    idx = int(choice)-1
    if idx < 0 or idx >= len(lst):
        print("[!] Out of range.\n"); return
    entry = lst[idx]
    print("\n--- ENTRY ---")
    print("Label   :", entry.get("label"))
    print("Username:", entry.get("username"))
    print("Password:", entry.get("password"))
    print("-------------\n")

# Delete One Password Method
def delete_one(fernet):
    """Delete a single entry by its number."""
    print("\n=== DELETE ONE PASSWORD ===")
    lst = load_list(fernet)
    if lst is None:
        print("[!] Cannot access database (wrong key or corrupted). Choose Reset DB.\n"); return
    if not lst:
        print("[!] No saved passwords.\n"); return
    for i, e in enumerate(lst, start=1):
        print(f"[{i}] {e.get('label','<no-label>')}")
    choice = input("\nEnter number to delete (or press Enter to cancel): ").strip()
    if not choice:
        print("[*] Cancelled.\n"); return
    if not choice.isdigit():
        print("[!] Invalid.\n"); return
    idx = int(choice)-1
    if idx < 0 or idx >= len(lst):
        print("[!] Out of range.\n"); return
    confirm = input(f"Delete '{lst[idx].get('label')}' ? (y/N): ").strip().lower()
    if confirm != "y":
        print("[*] Cancelled.\n"); return
    del lst[idx]
    save_list(lst, fernet)
    print("[+] Entry deleted.\n")

# Delete All Passwords Method
def delete_all(fernet):
    """Delete the encrypted DB file (wipes all saved entries)."""
    print("\n=== DELETE ALL PASSWORDS ===")
    confirm = input("Type DELETE to confirm wiping all saved passwords: ").strip()
    if confirm != "DELETE":
        print("[*] Cancelled.\n"); return
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print("[+] All passwords deleted.\n")
# Method to reset database
def reset_database():
    """Delete both key and DB file to reset the store (start fresh)."""
    print("\n=== RESET DATABASE (FULL WIPE) ===")
    confirm = input("Type RESET to confirm wiping key and DB: ").strip()
    if confirm != "RESET":
        print("[*] Cancelled.\n"); return
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
    print("[+] Database and key removed. A new key will be created on next use.\n")

# Main interface loop Method
def manager_interface():
    """
    Very small and simple interactive manager CLI.
    Loads/creates key and provides menu for basic operations.
    """
    ensure_data()
    key = load_or_create_key()
    fernet = Fernet(key)

    while True:
        print("""
[1] Add new password
[2] View saved labels
[3] Show password details
[4] Delete one password
[5] Delete ALL passwords
[6] Reset database (wipe key + DB)
[7] Return to main menu
""")
        choice = input("Choose (1-7): ").strip()
        if choice == "1":
            add_password(fernet)
        elif choice == "2":
            view_labels(fernet)
        elif choice == "3":
            show_details(fernet)
        elif choice == "4":
            delete_one(fernet)
        elif choice == "5":
            delete_all(fernet)
        elif choice == "6":
            reset_database()
        elif choice == "7":
            print("[*] Returning to main menu.\n")
            break
        else:
            print("[!] Invalid option. Please choose 1-7.\n")
