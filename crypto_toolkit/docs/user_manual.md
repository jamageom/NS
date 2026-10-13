# User Manual — Classical Cryptography Toolkit
## Network Security | Final Year ECM 2026-27

---

## 1. Installation

### Prerequisites
- Python 3.10 or higher
- `tkinter` (included with most Python installations on Windows)

### Steps
```powershell
# 1. Unzip/clone the project
unzip classical-crypto-toolkit.zip
# OR
git clone https://github.com/[USERNAME]/classical-crypto-toolkit.git

# 2. Navigate into the toolkit folder
cd crypto_toolkit

# 3. Verify Python version
python --version
# Expected: Python 3.10.x or higher

# 4. No pip install required for core functionality
# Optional: install pytest for structured test runs
pip install pytest
```

---

## 2. Running the CLI

```powershell
python main.py
```

You will first be prompted for a **password**:

```
============================================
  CLASSICAL CRYPTOGRAPHY TOOLKIT
  Password Required
============================================
  (Default password: crypto2026)

  Enter Password (attempt 1/3):
```

Enter: **`crypto2026`** (the default)

> ⚠️ You have **3 attempts**. After 3 failures the program exits for security.

After successful login, the main menu appears.

---

## 3. Running the GUI

```powershell
python main.py --gui
```

The Tkinter GUI opens with:
- **Cipher Tab** — Select cipher, enter text and key, encrypt/decrypt
- **Compare Tab** — Run all 8 ciphers on one plaintext

> Note: No password prompt in GUI mode (add authentication as needed).

---

## 4. Menu Options — Detailed Guide

---

### Option 1: Caesar Cipher

```
  Enter Plaintext : HELLO WORLD
  Enter Key (integer shift) : 3

  Plaintext  : HELLO WORLD
  Ciphertext : KHOOR ZRUOG
  Decrypted  : HELLO WORLD
  Enc. Time  : 0.0023 ms
```

**Key rules:**
- Any integer (positive or negative)
- Key is automatically reduced mod 26 (so key=29 equals key=3)
- Spaces and punctuation are preserved

---

### Option 2: Monoalphabetic Cipher

```
  Enter Plaintext : HELLO
  Key options:
    A) Enter your own 26-letter key
    B) Auto-generate a random key
  Select [A/B] : B
  Generated Key : QWERTYUIOPASDFGHJKLZXCVBNM
```

**Key rules:**
- Must be exactly 26 unique uppercase letters
- All 26 letters of the alphabet, each used exactly once
- Spaces and punctuation preserved in output

---

### Option 3: Playfair Cipher

```
  Enter Plaintext : HIDE THE GOLD
  Enter Keyword : MONARCHY

  Playfair Matrix:
  M O N A R
  C H Y B D
  E F G I K
  L P Q S T
  U V W X Z
```

**Key rules:**
- Any alphabetic word/phrase
- I and J are treated as the same letter (J→I in plaintext)
- Repeated letters in a digraph get `X` inserted
- Odd-length plaintext gets `X` appended

---

### Option 4: Hill Cipher

```
  Enter Plaintext : HELLO
  Enter key matrix as comma-separated integers:
    2x2 example: 3,7,2,5
    3x3 example: 6,24,1,13,16,10,20,17,15
  Enter Key Matrix : 3,7,2,5

  Key Matrix:
      3    7
      2    5
  Inverse Key Matrix (mod 26):
      5   19
     24    3
```

**Key rules:**
- 4 integers for 2×2, 9 integers for 3×3
- `gcd(det(matrix), 26)` must equal 1 (matrix invertible mod 26)
- If invalid: `[Error] Key matrix determinant is not invertible mod 26`
- Valid 2×2 example: `3,7,2,5` (det = 1)
- Valid 3×3 example: `6,24,1,13,16,10,20,17,15`

---

### Option 5: Vigenère Cipher

```
  Enter Plaintext : ATTACK AT DAWN
  Enter Keyword (letters only) : LEMON

  Plaintext  : ATTACK AT DAWN
  Ciphertext : LXFOPV EF RNHR
  Decrypted  : ATTACK AT DAWN
```

**Key rules:**
- Letters only (A-Z), no numbers or spaces
- Keyword repeats over the plaintext
- Key does NOT advance on spaces/punctuation

---

### Option 6: One-Time Pad

```
  Enter Plaintext : HELLO
  Key options:
    A) Enter your own key
    B) Auto-generate a secure random key
  Select [A/B] : B
  Generated Key : XMCKL
  ⚠️  Save this key securely! It cannot be recovered.
```

**Key rules:**
- Letters only (A-Z)
- Must be **at least as long** as the number of letters in plaintext
- The toolkit warns if you reuse a key in the same session
- **NEVER reuse an OTP key** — doing so breaks security

---

### Option 7: Rail Fence Cipher

```
  Enter Plaintext : WEAREDISCOVERED
  Enter Number of Rails (≥ 2) : 3
  Show zig-zag grid? [y/n] : y

  Rail 0: W . . . E . . . C . . . R . .
  Rail 1: . E . R . D . S . O . E . E .
  Rail 2: . . A . . . I . . . V . . . D

  Ciphertext : WECRERDSOEEAIVD
```

**Key rules:**
- Integer ≥ 2
- All characters (including spaces) are included in the zig-zag

---

### Option 8: Columnar Transposition

```
  Enter Plaintext : WEAREDISCOVEREDFLEEATONCE
  Enter Keyword : ZEBRAS

  Key: Z  E  B  R  A  S
  ----------------------
  W  E  A  R  E  D
  I  S  C  O  V  E
  R  E  D  F  L  E
  A  T  O  N  C  E
  Read order: 4 → 1 → 2 → 3 → 5 → 0
```

**Key rules:**
- Letters only
- Columns read in alphabetical order of key letters
- Plaintext padded with `X` to fill the grid

---

### Option 9: Compare Algorithms

Enter one plaintext — all 8 ciphers run with sensible default keys and a table shows:
- Cipher name, type, key used, ciphertext
- Encryption time, decryption time
- Round-trip verification (Yes/No)

Plus a brief strength/key-space comparison note.

---

### Option 10: Encrypt Text File

```
  Enter input file path : samples/sample_plain.txt
  (Loaded 743 characters)
  Select cipher: 1. Caesar
  Enter shift key (integer) : 5

  Cipher    : Caesar
  Enc. Time : 0.0312 ms
  Output    : samples/sample_plain_encrypted.txt
```

---

### Option 11: Decrypt Text File

```
  Enter encrypted file path : samples/sample_plain_encrypted.txt
  Select cipher: 1. Caesar
  Enter shift key : 5

  Cipher    : Caesar
  Dec. Time : 0.0298 ms
  Output    : samples/sample_plain_encrypted_decrypted.txt
```

---

### Option 12: Help

Displays key formats, examples, and tips for every cipher.

---

### Option 13: Exit

```
  Thank you for using the Classical Cryptography Toolkit!
  Goodbye! Stay secure. 🔒
```

---

## 5. Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'tkinter'` | Install Python with tkinter support (Windows: standard installer includes it) |
| `[Error] Monoalphabetic key must be exactly 26 letters` | Provide all 26 letters exactly once, or use auto-generate |
| `[Error] Key matrix determinant is not invertible mod 26` | Choose a different 2×2 or 3×3 matrix; try `3,7,2,5` |
| `[Error] OTP key is too short` | Use auto-generate; OTP key must have ≥ |plaintext alpha chars| letters |
| `[Error] File not found` | Check the file path; use absolute paths if relative fails |
| Password rejected 3 times → program exits | Restart and use: `crypto2026` |
| GUI window does not appear | Ensure `tkinter` is available: `python -c "import tkinter"` |

---

## 6. Changing the Password

Edit `main.py`, find the line:
```python
_PASSWORD_HASH = hashlib.sha256("crypto2026".encode()).hexdigest()
```
Replace `"crypto2026"` with your new password. The hash is computed automatically at startup.

---

*Classical Cryptography Toolkit — User Manual — Final Year ECM 2026-27*
