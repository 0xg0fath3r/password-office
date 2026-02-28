"""
modules/policy_checker.py
Password Policy Checker module for Password Office.
Verifies a password against a configurable security policy.
Author: Ogbonna Samuel (0xg0fath3r)
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Policy rules loaded from .env — falls back to secure defaults
MIN_LENGTH      = int(os.getenv("POLICY_MIN_LENGTH",      8))
MAX_LENGTH      = int(os.getenv("POLICY_MAX_LENGTH",      128))
REQUIRE_UPPER   =     os.getenv("POLICY_REQUIRE_UPPER",   "true").lower()  == "true"
REQUIRE_LOWER   =     os.getenv("POLICY_REQUIRE_LOWER",   "true").lower()  == "true"
REQUIRE_DIGIT   =     os.getenv("POLICY_REQUIRE_DIGIT",   "true").lower()  == "true"
REQUIRE_SYMBOL  =     os.getenv("POLICY_REQUIRE_SYMBOL",  "true").lower()  == "true"


def policy_interface():
    """
    Check a password against the active security policy.
    Policy rules can be customised via .env variables.
    """
    print("\n" + "=" * 50)
    print("        PASSWORD POLICY CHECKER")
    print("=" * 50)
    print(f"\n  Active Policy:")
    print(f"  - Min length   : {MIN_LENGTH}")
    print(f"  - Max length   : {MAX_LENGTH}")
    print(f"  - Uppercase    : {'Required' if REQUIRE_UPPER  else 'Optional'}")
    print(f"  - Lowercase    : {'Required' if REQUIRE_LOWER  else 'Optional'}")
    print(f"  - Digits       : {'Required' if REQUIRE_DIGIT  else 'Optional'}")
    print(f"  - Symbols      : {'Required' if REQUIRE_SYMBOL else 'Optional'}")
    print()

    pwd = input("[?] Enter password to check: ")

    if not pwd:
        print("[!] No password entered.\n")
        return

    # Define checks based on policy
    checks = {
        f"At least {MIN_LENGTH} characters"    : len(pwd) >= MIN_LENGTH,
        f"No more than {MAX_LENGTH} characters": len(pwd) <= MAX_LENGTH,
        "Contains uppercase letter"            : any(c.isupper() for c in pwd) if REQUIRE_UPPER  else True,
        "Contains lowercase letter"            : any(c.islower() for c in pwd) if REQUIRE_LOWER  else True,
        "Contains a digit"                     : any(c.isdigit() for c in pwd) if REQUIRE_DIGIT  else True,
        "Contains a symbol"                    : any(not c.isalnum() for c in pwd) if REQUIRE_SYMBOL else True,
    }

    # Print results
    print("\n" + "-" * 50)
    print("  POLICY CHECK RESULTS")
    print("-" * 50)

    all_passed = True
    for rule, passed in checks.items():
        mark = "[✔]" if passed else "[✘]"
        print(f"  {mark} {rule}")
        if not passed:
            all_passed = False

    print("-" * 50)
    if all_passed:
        print("  ✅ Password PASSES all policy requirements!")
    else:
        print("  ❌ Password FAILS one or more policy requirements.")
    print("-" * 50 + "\n")


def main():
    policy_interface()
