import random
import string

# Method for Password Generation
def generator_interface():
    print("\n=== PASSWORD GENERATOR ===")
    # Prompt user for length; protect against invalid input
    try:
        length = int(input("Enter password length (e.g., 12): ").strip())
    except Exception:
        print("[!] Invalid number. Please enter a numeric length.\n")
        return

    if length < 4:
        # very small minimum to avoid useless tiny passwords
        print("[!] Length too short. Choose at least 4.\n")
        return

    # Character set includes lowercase, uppercase, digits and punctuation
    chars = string.ascii_letters + string.digits + string.punctuation

    # Build password using random.choice 
    password = ''.join(random.choice(chars) for _ in range(length))

    # Show result clearly
    print("\n[+] Generated password:\n")
    print(password + "\n")
