# Policy Checker Method

def policy_interface():
    """
    Ask user for a password and test the following:
    - Minimum 8 characters
    - Contains uppercase
    - Contains lowercase
    - Contains digits
    - Contains symbols
    Print pass/fail for each rule.
    """
    print("\n=== PASSWORD POLICY CHECKER ===")
    pwd = input("Enter password to check: ")

    # Define checks
    checks = {
        "At least 8 characters": len(pwd) >= 8,
        "Has uppercase letter": any(c.isupper() for c in pwd),
        "Has lowercase letter": any(c.islower() for c in pwd),
        "Contains a digit": any(c.isdigit() for c in pwd),
        "Contains a symbol": any(not c.isalnum() for c in pwd),
    }

    # Print results
    print("\n--- POLICY CHECK RESULTS ---")
    for rule, ok in checks.items():
        mark = "[✔]" if ok else "[✘]"
        print(f"{mark} {rule}")
    print()
