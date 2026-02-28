# strength Checker Method

def strength_checker_interface():
    """
    Ask for password, evaluate basic checks:
    - length >= 8
    - has upper, lower, digit, symbol
    Score and return WEAK / MEDIUM / STRONG
    """
    print("\n=== PASSWORD STRENGTH CHECKER ===")
    pwd = input("Enter password to check: ").strip()

    # Quick checks for password composition
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_symbol = any(not c.isalnum() for c in pwd)

    # Score increases for each positive property
    score = 0
    if length >= 8:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    # Map score to textual strength
    if score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    # Print result with basic reasoning for presentation
    print(f"\n[+] Strength: {strength}")
    print(f"    - Length: {length}  Upper:{has_upper} Lower:{has_lower} Digit:{has_digit} Symbol:{has_symbol}\n")
