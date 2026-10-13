"""
Classical Cryptography Toolkit
================================
Main entry point. Provides:
  - Password protection (SHA-256, 3 attempts).
  - Menu-driven CLI with all 8 ciphers + utility modules.
  - Optional Tkinter GUI via --gui flag.

Usage:
    python main.py          # Launch CLI
    python main.py --gui    # Launch GUI
"""

import sys
import os
import hashlib
import time

# Ensure the crypto_toolkit package is importable when running from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers import (
    CaesarCipher, MonoalphabeticCipher, PlayfairCipher,
    HillCipher, VigenereCipher, OneTimePad,
    RailFenceCipher, ColumnarCipher,
)
from utils.file_ops import load_text_file, save_text_file, get_output_path
from utils.timing import time_operation, format_time
from utils.validators import (
    validate_non_empty, validate_integer, validate_rails,
    validate_alpha_key, validate_mono_key,
    validate_hill_matrix_string, validate_otp_key, validate_file_path,
)

# ----------------------------------------------
# Password Protection
# ----------------------------------------------
# Default password: crypto2026  (SHA-256 stored)
_PASSWORD_HASH = "a3f3e9e9e8b9c7d5c3b0e5f7a4d8c2b1e0f6a3c9d7b2e8f5a1d4c6b3e7f2a5d9"

# Compute proper hash for default password "crypto2026"
_PASSWORD_HASH = hashlib.sha256("crypto2026".encode()).hexdigest()

MAX_ATTEMPTS = 3

# ----------------------------------------------
# Cipher instances (singletons)
# ----------------------------------------------
_caesar = CaesarCipher()
_mono   = MonoalphabeticCipher()
_play   = PlayfairCipher()
_hill   = HillCipher()
_vig    = VigenereCipher()
_otp    = OneTimePad()
_rail   = RailFenceCipher()
_col    = ColumnarCipher()


# ----------------------------------------------
# Helper UI functions
# ----------------------------------------------

def divider(char: str = "=", width: int = 44) -> None:
    print(char * width)


def header(title: str = "CLASSICAL CRYPTOGRAPHY TOOLKIT") -> None:
    divider()
    print(f" {title}")
    divider()


def pause() -> None:
    """Wait for the user to press Enter before returning to menu."""
    input("\n  Press Enter to return to the menu...")


def get_input(prompt: str) -> str:
    """Read a line of user input, stripping surrounding whitespace."""
    return input(f"  {prompt}").strip()


def print_result(plaintext: str, ciphertext: str, decrypted: str,
                 enc_time: float, dec_time: float) -> None:
    """Print the standard encrypt/decrypt result block."""
    print()
    print(f"  Plaintext  : {plaintext}")
    print(f"  Ciphertext : {ciphertext}")
    print(f"  Decrypted  : {decrypted}")
    print(f"  Enc. Time  : {format_time(enc_time)}")
    print(f"  Dec. Time  : {format_time(dec_time)}")


# ----------------------------------------------
# Menu display
# ----------------------------------------------

def show_menu() -> None:
    print()
    divider()
    print(" CLASSICAL CRYPTOGRAPHY TOOLKIT")
    divider()
    print("SUBSTITUTION CIPHERS")
    print("  1. Caesar Cipher")
    print("  2. Monoalphabetic Cipher")
    print("  3. Playfair Cipher")
    print("  4. Hill Cipher")
    print("  5. Vigenère (Polyalphabetic) Cipher")
    print("  6. One-Time Pad")
    print("TRANSPOSITION CIPHERS")
    print("  7. Rail Fence Cipher")
    print("  8. Columnar Transposition Cipher")
    print("UTILITY MODULES")
    print("  9. Compare Algorithms")
    print(" 10. Encrypt Text File")
    print(" 11. Decrypt Text File")
    print(" 12. Help")
    print(" 13. Exit")
    divider()


# ----------------------------------------------
# Cipher handlers
# ----------------------------------------------

def handle_caesar() -> None:
    header("CAESAR CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")
        key_str   = get_input("Enter Key (integer shift) : ")
        key       = validate_integer(key_str, "Caesar key")

        ciphertext, enc_t = time_operation(_caesar.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_caesar.decrypt, ciphertext, key)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_monoalphabetic() -> None:
    header("MONOALPHABETIC CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")

        print("  Key options:")
        print("    A) Enter your own 26-letter key")
        print("    B) Auto-generate a random key")
        choice = get_input("Select [A/B] : ").upper()

        if choice == 'B':
            key = _mono.generate_key()
            print(f"  Generated Key : {key}")
        else:
            key = get_input("Enter 26-letter Key : ")
        key = validate_mono_key(key)

        ciphertext, enc_t = time_operation(_mono.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_mono.decrypt, ciphertext, key)

        print(f"\n  Key Used   : {key}")
        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_playfair() -> None:
    header("PLAYFAIR CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")
        key       = get_input("Enter Keyword : ")
        validate_non_empty(key, "Keyword")

        print()
        print(_play.get_matrix_str(key))

        ciphertext, enc_t = time_operation(_play.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_play.decrypt, ciphertext, key)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_hill() -> None:
    header("HILL CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")

        print("  Enter key matrix as comma-separated integers:")
        print("    2x2 example: 3,7,2,5")
        print("    3x3 example: 6,24,1,13,16,10,20,17,15")
        key_str = get_input("Enter Key Matrix : ")
        matrix  = validate_hill_matrix_string(key_str)

        print()
        print(_hill.matrix_str(matrix))
        print(_hill.get_inverse_str(matrix))

        ciphertext, enc_t = time_operation(_hill.encrypt, plaintext, matrix)
        decrypted,  dec_t = time_operation(_hill.decrypt, ciphertext, matrix)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_vigenere() -> None:
    header("VIGENÈRE CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")
        key       = get_input("Enter Keyword (letters only) : ")
        key       = validate_alpha_key(key, "Vigenère key")

        ciphertext, enc_t = time_operation(_vig.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_vig.decrypt, ciphertext, key)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_otp() -> None:
    header("ONE-TIME PAD")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")

        print("  Key options:")
        print("    A) Enter your own key (≥ number of letters in plaintext)")
        print("    B) Auto-generate a secure random key")
        choice = get_input("Select [A/B] : ").upper()

        if choice == 'B':
            key = _otp.generate_key(plaintext)
            print(f"  Generated Key : {key}")
            print("  [!]  Save this key securely! It cannot be recovered.")
        else:
            key = get_input("Enter Key (letters only) : ")

        ciphertext, enc_t = time_operation(_otp.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_otp.decrypt, ciphertext, key)

        print(f"\n  Key Used   : {key}")
        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_railfence() -> None:
    header("RAIL FENCE CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")
        rails_str = get_input("Enter Number of Rails (≥ 2) : ")
        rails     = validate_rails(rails_str)

        show_grid = get_input("Show zig-zag grid? [y/n] : ").lower() == 'y'
        if show_grid:
            print()
            print(_rail.get_zig_zag_grid(plaintext.upper(), rails))

        ciphertext, enc_t = time_operation(_rail.encrypt, plaintext, rails)
        decrypted,  dec_t = time_operation(_rail.decrypt, ciphertext, rails)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_columnar() -> None:
    header("COLUMNAR TRANSPOSITION CIPHER")
    try:
        plaintext = get_input("Enter Plaintext : ")
        validate_non_empty(plaintext, "Plaintext")
        key       = get_input("Enter Keyword : ")
        key       = validate_alpha_key(key, "Columnar key")

        # Show grid before encrypting
        padded = plaintext.upper()
        while len(padded) % len(key) != 0:
            padded += 'X'
        print()
        print(_col.get_grid_str(padded, key))

        ciphertext, enc_t = time_operation(_col.encrypt, plaintext, key)
        decrypted,  dec_t = time_operation(_col.decrypt, ciphertext, key)

        print_result(plaintext.upper(), ciphertext, decrypted, enc_t, dec_t)
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


# ----------------------------------------------
# Utility: Compare Algorithms (Option 9)
# ----------------------------------------------

_DEFAULT_KEYS = {
    "Caesar":    3,
    "Mono":      "QWERTYUIOPASDFGHJKLZXCVBNM",
    "Playfair":  "KEYWORD",
    "Hill":      "3,7,2,5",
    "Vigenère":  "KEY",
    "OTP":       None,   # generated per plaintext
    "RailFence": 3,
    "Columnar":  "ZEBRA",
}


def handle_compare() -> None:
    header("COMPARE ALGORITHMS")
    try:
        plaintext = get_input("Enter Plaintext (for all ciphers) : ")
        validate_non_empty(plaintext, "Plaintext")

        print("\n  Running all 8 ciphers with default keys...\n")

        otp_key = _otp.generate_key(plaintext)
        hill_matrix = validate_hill_matrix_string(_DEFAULT_KEYS["Hill"])

        configs = [
            ("Caesar",    "Substitution",  _caesar.encrypt, _caesar.decrypt, _DEFAULT_KEYS["Caesar"]),
            ("Mono",      "Substitution",  _mono.encrypt,   _mono.decrypt,   _DEFAULT_KEYS["Mono"]),
            ("Playfair",  "Substitution",  _play.encrypt,   _play.decrypt,   _DEFAULT_KEYS["Playfair"]),
            ("Hill",      "Substitution",  _hill.encrypt,   _hill.decrypt,   hill_matrix),
            ("Vigenère",  "Substitution",  _vig.encrypt,    _vig.decrypt,    _DEFAULT_KEYS["Vigenère"]),
            ("OTP",       "Substitution",  _otp.encrypt,    _otp.decrypt,    otp_key),
            ("RailFence", "Transposition", _rail.encrypt,   _rail.decrypt,   _DEFAULT_KEYS["RailFence"]),
            ("Columnar",  "Transposition", _col.encrypt,    _col.decrypt,    _DEFAULT_KEYS["Columnar"]),
        ]

        # Table header
        col_w = [12, 14, 28, 30, 12, 12, 12]
        headers = ["Algorithm", "Type", "Key Used", "Ciphertext", "Enc Time", "Dec Time", "Round-trip"]
        sep = "+" + "+".join("-" * w for w in col_w) + "+"
        row_fmt = "|" + "|".join(f"{{:<{w}}}" for w in col_w) + "|"

        print(sep)
        print(row_fmt.format(*headers))
        print(sep)

        for name, typ, enc_fn, dec_fn, key in configs:
            try:
                cipher_text, enc_t = time_operation(enc_fn, plaintext, key)
                decrypted,   dec_t = time_operation(dec_fn, cipher_text, key)

                # Round-trip check: compare normalised texts
                orig = ''.join(ch for ch in plaintext.upper() if ch.isalpha())
                got  = ''.join(ch for ch in decrypted.upper() if ch.isalpha())
                # Strip trailing X padding
                round_trip = "Yes" if got.startswith(orig) or orig == got else "No"

                key_str    = str(key)[:26] + ("…" if len(str(key)) > 26 else "")
                cipher_str = cipher_text[:28] + ("…" if len(cipher_text) > 28 else "")

                print(row_fmt.format(
                    name[:12], typ[:14], key_str[:28], cipher_str[:30],
                    format_time(enc_t)[:12], format_time(dec_t)[:12], round_trip[:12]
                ))
            except Exception as ex:
                print(row_fmt.format(name, typ, str(key)[:28], f"ERROR: {ex}"[:30], "-", "-", "No"))
            print(sep)

        print()
        print("  Strength & Key Space Comparison:")
        print("  -----------------------------------------------------------------")
        notes = [
            ("Caesar",    "Very weak. Key space = 25.",                          "Brute-forceable in seconds."),
            ("Mono",      "Weak. Key space ≈ 26! ≈ 4×10²⁶.",                    "Vulnerable to frequency analysis."),
            ("Playfair",  "Moderate. Digraph; harder than mono.",                "Still breakable with ~20+ chars."),
            ("Hill",      "Moderate-strong. Matrix space large.",                "Vulnerable to known-plaintext."),
            ("Vigenère",  "Moderate. Key space = 26^|key|.",                     "Broken by Kasiski/IC analysis."),
            ("OTP",       "Perfect secrecy IF key is truly random & never reused.", "Unbreakable in theory."),
            ("RailFence", "Very weak. Key space = small int.",                   "Easily brute-forced."),
            ("Columnar",  "Weak-moderate. Key space = |key|!.",                  "Broken by anagramming."),
        ]
        for name, strength, note in notes:
            print(f"  {name:<12}: {strength}")
            print(f"              {note}")
        print()
    except ValueError as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


# ----------------------------------------------
# Utility: Encrypt / Decrypt File (Options 10/11)
# ----------------------------------------------

_CIPHER_MAP = {
    "1": ("Caesar",    _caesar),
    "2": ("Mono",      _mono),
    "3": ("Playfair",  _play),
    "4": ("Hill",      _hill),
    "5": ("Vigenère",  _vig),
    "6": ("OTP",       _otp),
    "7": ("RailFence", _rail),
    "8": ("Columnar",  _col),
}


def _prompt_cipher_and_key(mode: str) -> tuple:
    """Return (cipher_name, cipher_instance, key) from user input."""
    print("  Select cipher:")
    for num, (name, _) in _CIPHER_MAP.items():
        print(f"    {num}. {name}")
    choice = get_input("Enter cipher number [1-8] : ")
    if choice not in _CIPHER_MAP:
        raise ValueError(f"Invalid cipher selection '{choice}'.")
    name, cipher = _CIPHER_MAP[choice]

    # Key prompts per cipher
    if name == "Caesar":
        key = validate_integer(get_input("Enter shift key (integer) : "), "Key")
    elif name == "Mono":
        k = get_input("Enter 26-letter key (or press Enter to auto-generate) : ")
        key = _mono.generate_key() if not k else validate_mono_key(k)
        print(f"  Key: {key}")
    elif name in ("Playfair", "Vigenère", "Columnar"):
        key = validate_alpha_key(get_input(f"Enter keyword : "), "Key")
    elif name == "Hill":
        key_str = get_input("Enter comma-separated matrix values (e.g. 3,7,2,5) : ")
        key = validate_hill_matrix_string(key_str)
    elif name == "OTP":
        k = get_input("Enter OTP key (or press Enter to auto-generate) : ")
        if not k:
            key = _otp.generate_key("")   # placeholder; real length set later
            print(f"  Generated key stub: {key} (will be extended as needed)")
        else:
            key = k.upper()
    elif name == "RailFence":
        key = validate_rails(get_input("Enter number of rails : "))
    else:
        key = get_input("Enter key : ")

    return name, cipher, key


def handle_encrypt_file() -> None:
    header("ENCRYPT TEXT FILE")
    try:
        filepath = validate_file_path(get_input("Enter input file path : "))
        content  = load_text_file(filepath)
        print(f"\n  Loaded {len(content)} characters from '{filepath}'.")

        name, cipher, key = _prompt_cipher_and_key("encrypt")

        # OTP: regenerate key to correct length
        if name == "OTP":
            key = _otp.generate_key(content)
            print(f"  OTP Key (SAVE THIS): {key}")

        ciphertext, enc_t = time_operation(cipher.encrypt, content, key)
        out_path = get_output_path(filepath, "_encrypted")
        save_text_file(out_path, ciphertext)

        print(f"\n  Cipher     : {name}")
        print(f"  Enc. Time  : {format_time(enc_t)}")
        print(f"  Output     : {out_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


def handle_decrypt_file() -> None:
    header("DECRYPT TEXT FILE")
    try:
        filepath = validate_file_path(get_input("Enter encrypted file path : "))
        content  = load_text_file(filepath)
        print(f"\n  Loaded {len(content)} characters from '{filepath}'.")

        name, cipher, key = _prompt_cipher_and_key("decrypt")

        decrypted, dec_t = time_operation(cipher.decrypt, content, key)
        out_path = get_output_path(filepath, "_decrypted")
        save_text_file(out_path, decrypted)

        print(f"\n  Cipher     : {name}")
        print(f"  Dec. Time  : {format_time(dec_t)}")
        print(f"  Output     : {out_path}")
    except (ValueError, FileNotFoundError) as e:
        print(f"\n  [Error] {e}")
    finally:
        pause()


# ----------------------------------------------
# Utility: Help (Option 12)
# ----------------------------------------------

_HELP_TEXT = """
  +-----------------------------------------------------------------+
  |              CLASSICAL CRYPTOGRAPHY TOOLKIT - HELP              |
  +-----------------------------------------------------------------+

  1. CAESAR CIPHER
     Key format : Integer (e.g. 5). Negative values shift left.
     Example    : Plaintext = HELLO, Key = 3 -> Ciphertext = KHOOR

  2. MONOALPHABETIC CIPHER
     Key format : 26 unique uppercase letters (permutation of A-Z).
     Example    : Key = QWERTYUIOPASDFGHJKLZXCVBNM
                  A->Q, B->W, C->E, …
     Tip        : Choose 'Auto-generate' to get a random valid key.

  3. PLAYFAIR CIPHER
     Key format : Any word/phrase (letters only), e.g. KEYWORD
     Notes      : I and J are treated as the same letter.
                  Repeated digraph letters get an X inserted.
                  Odd-length plaintext gets X appended.

  4. HILL CIPHER
     Key format : 4 comma-separated integers (2×2) or 9 (3×3).
     Example    : 3,7,2,5  (2×2)   or   6,24,1,13,16,10,20,17,15 (3×3)
     Constraint : det(K) must be coprime with 26.

  5. VIGENÈRE CIPHER
     Key format : Letters only (e.g. KEY). Repeats over plaintext.
     Notes      : Non-letter characters are preserved as-is.

  6. ONE-TIME PAD
     Key format : Uppercase letters, at least as long as the plaintext.
     Notes      : NEVER reuse the key. Use auto-generate for security.

  7. RAIL FENCE CIPHER
     Key format : Integer ≥ 2 (number of rails).
     Example    : Plaintext = WEAREDISCOVERED, Rails = 3
                  Ciphertext = WECRLTEERDSOEIA

  8. COLUMNAR TRANSPOSITION
     Key format : Any word (letters only), e.g. ZEBRA
     Notes      : Columns are read in alphabetical order of key letters.
                  Plaintext is padded with X to fill the grid.

  UTILITY OPTIONS:
    9  - Compare all 8 ciphers on one plaintext (with timing).
    10 - Encrypt a text file with any cipher.
    11 - Decrypt an encrypted file.
    12 - Show this help screen.
    13 - Exit.
"""


def handle_help() -> None:
    header("HELP")
    print(_HELP_TEXT)
    pause()


# ----------------------------------------------
# Password Gate
# ----------------------------------------------

def password_gate() -> bool:
    """
    Prompt for the toolkit password (SHA-256 verified).
    Allows MAX_ATTEMPTS attempts before exiting.

    Returns:
        True if authenticated, exits on failure.
    """
    print()
    divider("=", 44)
    print("  CLASSICAL CRYPTOGRAPHY TOOLKIT")
    print("  Password Required")
    divider("=", 44)
    print("  (Default password: crypto2026)")
    print()
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            pwd = input(f"  Enter Password (attempt {attempt}/{MAX_ATTEMPTS}): ")
        except (EOFError, KeyboardInterrupt):
            print("\n  Exiting...")
            sys.exit(0)

        if hashlib.sha256(pwd.encode()).hexdigest() == _PASSWORD_HASH:
            print("\n  [OK] Access granted. Welcome!\n")
            return True
        else:
            remaining = MAX_ATTEMPTS - attempt
            if remaining:
                print(f"  ✗ Incorrect password. {remaining} attempt(s) remaining.")
            else:
                print("  ✗ Too many incorrect attempts. Exiting for security.")
                sys.exit(1)
    return False   # unreachable


# ----------------------------------------------
# Main CLI loop
# ----------------------------------------------

_MENU_DISPATCH = {
    "1":  handle_caesar,
    "2":  handle_monoalphabetic,
    "3":  handle_playfair,
    "4":  handle_hill,
    "5":  handle_vigenere,
    "6":  handle_otp,
    "7":  handle_railfence,
    "8":  handle_columnar,
    "9":  handle_compare,
    "10": handle_encrypt_file,
    "11": handle_decrypt_file,
    "12": handle_help,
}


def run_cli() -> None:
    """Main CLI loop."""
    password_gate()
    while True:
        show_menu()
        try:
            choice = input("Enter your Choice : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye! Stay secure.")
            break

        if choice == "13":
            print("\n  Thank you for using the Classical Cryptography Toolkit!")
            print("  Goodbye! Stay secure. [LOCK]\n")
            break
        elif choice in _MENU_DISPATCH:
            _MENU_DISPATCH[choice]()
        else:
            print(f"\n  [!] Invalid option '{choice}'. Please enter a number between 1 and 13.")
            time.sleep(0.5)


# ----------------------------------------------
# Entry point
# ----------------------------------------------

if __name__ == "__main__":
    if "--gui" in sys.argv:
        # Launch the Tkinter GUI
        try:
            import importlib.util, os as _os
            gui_path = _os.path.join(_os.path.dirname(__file__), "gui.py")
            spec = importlib.util.spec_from_file_location("gui", gui_path)
            gui_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gui_mod)
            gui_mod.launch()
        except Exception as ex:
            print(f"  [Error] Could not launch GUI: {ex}")
            sys.exit(1)
    else:
        run_cli()
