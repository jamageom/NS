# Classical Cryptography Toolkit 🔐
> **Final Year ECM (2026-27) · Network Security Mini Project**

A complete, modular Python toolkit implementing **8 classical ciphers** with a menu-driven CLI, Tkinter GUI, file encryption, algorithm comparison, timing analysis, and comprehensive unit tests.

---

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Requirements](#setup--requirements)
- [Default Password](#default-password)
- [Running the CLI](#running-the-cli)
- [Running the GUI](#running-the-gui)
- [Cipher Overview](#cipher-overview)
- [Running Tests](#running-tests)
- [File Encryption/Decryption](#file-encryptiondecryption)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔒 Password gate | SHA-256 hash, 3 attempts, then exits |
| 8 ciphers | Caesar, Mono, Playfair, Hill, Vigenère, OTP, Rail Fence, Columnar |
| ⏱ Timing | Encryption/decryption time displayed for every operation |
| 📊 Compare | Run all 8 ciphers on one plaintext with a results table |
| 📂 File ops | Encrypt/decrypt any text file with any cipher |
| 🎲 Key gen | Auto-generate random keys for Monoalphabetic and OTP |
| 🖥 GUI | Tkinter GUI with dark theme, cipher dropdown, file load/save, compare tab |
| 🧪 Tests | 76 unit tests (round-trip, known vectors, edge cases) |

---

## 🗂 Project Structure

```
crypto_toolkit/
├── main.py                 # Menu-driven CLI entry point
├── gui.py                  # Tkinter GUI (launch with --gui)
├── requirements.txt        # No third-party deps for core
├── ciphers/
│   ├── __init__.py
│   ├── caesar.py           # Caesar shift cipher
│   ├── monoalphabetic.py   # Monoalphabetic substitution
│   ├── playfair.py         # Playfair digraph cipher
│   ├── hill.py             # Hill matrix cipher (2x2 / 3x3)
│   ├── vigenere.py         # Vigenère polyalphabetic
│   ├── otp.py              # One-Time Pad
│   ├── railfence.py        # Rail Fence transposition
│   └── columnar.py         # Columnar transposition
├── utils/
│   ├── file_ops.py         # Load/save text files
│   ├── timing.py           # perf_counter timing helpers
│   └── validators.py       # Input validation
├── tests/
│   └── test_ciphers.py     # 76 unittest cases
├── samples/
│   └── sample_plain.txt    # Demo plaintext file
└── docs/
    ├── mini_project_report.md
    ├── user_manual.md
    ├── demo_script.md
    └── presentation.md
```

---

## ⚙ Setup & Requirements

- **Python 3.10+** (standard library only — no pip installs needed)
- `tkinter` is included with most Python installations
- Optional: `pip install pytest` for structured test runs

```powershell
# Verify Python version
python --version          # Should be 3.10 or higher

# Clone / unzip and navigate
cd crypto_toolkit

# Run CLI (no install needed)
python main.py

# Run GUI
python main.py --gui
```

---

## 🔑 Default Password

```
crypto2026
```

The password is verified against a SHA-256 hash. You have **3 attempts** before the program exits.

To change the password, edit `main.py` line with `_PASSWORD_HASH`:
```python
_PASSWORD_HASH = hashlib.sha256("your_new_password".encode()).hexdigest()
```

---

## 🖥 Running the CLI

```powershell
python main.py
```

```
============================================
 CLASSICAL CRYPTOGRAPHY TOOLKIT
============================================
SUBSTITUTION CIPHERS
  1. Caesar Cipher
  2. Monoalphabetic Cipher
  3. Playfair Cipher
  4. Hill Cipher
  5. Vigenère (Polyalphabetic) Cipher
  6. One-Time Pad
TRANSPOSITION CIPHERS
  7. Rail Fence Cipher
  8. Columnar Transposition Cipher
UTILITY MODULES
  9. Compare Algorithms
 10. Encrypt Text File
 11. Decrypt Text File
 12. Help
 13. Exit
============================================
Enter your Choice :
```

---

## 🖼 Running the GUI

```powershell
python main.py --gui
```

The GUI features:
- Cipher selector dropdown
- Plaintext / output text boxes
- Key field + **Generate Random Key** button
- **Encrypt** / **Decrypt** buttons with execution time
- **Load File** / **Save Output** buttons
- **Compare tab** — run all 8 ciphers at once

---

## 🔐 Cipher Overview

| # | Cipher | Type | Key Format | Key Space |
|---|--------|------|------------|-----------|
| 1 | Caesar | Substitution | Integer (any) | 25 |
| 2 | Monoalphabetic | Substitution | 26 unique letters | ≈ 26! |
| 3 | Playfair | Substitution | Keyword (letters) | Large |
| 4 | Hill | Substitution | 4 or 9 comma-sep ints | Very large |
| 5 | Vigenère | Substitution | Alphabetic keyword | 26^|key| |
| 6 | OTP | Substitution | Random letters ≥ |plaintext| | Perfect |
| 7 | Rail Fence | Transposition | Integer ≥ 2 | Small |
| 8 | Columnar | Transposition | Keyword (letters) | |key|! |

### Mandatory Test Case
```
Cipher  : Caesar, Key = 5
Input   : NETWORK SECURITY
Output  : SJYBTWP XJHZWNYD
Decrypt : NETWORK SECURITY  ✓
```

---

## 🧪 Running Tests

```powershell
# Using unittest (no extra packages)
python tests/test_ciphers.py

# Using pytest (if installed)
python -m pytest tests/test_ciphers.py -v
```

**Result: 76 tests, 0 failures.**

---

## 📂 File Encryption/Decryption

Use menu options **10** and **11** in the CLI, or the Load/Save buttons in the GUI.

Output files are saved as:
- `filename_encrypted.txt`
- `filename_decrypted.txt`

---

## 👤 Student Details

| Field | Value |
|-------|-------|
| Name | [YOUR NAME] |
| Roll No. | [ROLL] |
| Batch | [BATCH] |
| Class | Final Year (ECM) |
| Year | 2026-27 |
| Course | Network Security |
| Date | October 2026 |

---

## 🔗 Links

- GitHub Repository: `https://github.com/[USERNAME]/classical-crypto-toolkit`
- Course: Network Security, Final Year ECM 2026-27
