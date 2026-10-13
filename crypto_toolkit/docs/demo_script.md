# Demo Video Script — Classical Cryptography Toolkit
## Total Duration: ~4 minutes 45 seconds

---

## SCENE 1 — Introduction (0:00–0:30)

**[Screen: Desktop / File Explorer showing project folder]**

> "Welcome to the Classical Cryptography Toolkit — a Network Security mini project 
> implementing eight classical ciphers in Python. The toolkit includes a CLI, a GUI, 
> file encryption, algorithm comparison, and 76 automated tests.
> Let me show you how it works."

**Action:** Open a terminal / PowerShell in the `crypto_toolkit/` folder.

---

## SCENE 2 — Launch & Password Gate (0:30–0:55)

**[Screen: Terminal]**

**Type:**
```
python main.py
```

**Expected output:**
```
============================================
  CLASSICAL CRYPTOGRAPHY TOOLKIT
  Password Required
============================================
  (Default password: crypto2026)

  Enter Password (attempt 1/3):
```

**Type:** `crypto2026`

**Expected:**
```
  ✓ Access granted. Welcome!
```

> "The toolkit is password-protected using SHA-256 hashing. 
> The default password is crypto2026."

---

## SCENE 3 — Caesar Cipher (0:55–1:25)

**[Screen: Main menu appears]**

**Type:** `1`

**Expected:**
```
============================================
 CAESAR CIPHER
============================================
  Enter Plaintext :
```

**Type:** `NETWORK SECURITY`

**Type key:** `5`

**Expected:**
```
  Plaintext  : NETWORK SECURITY
  Ciphertext : SJYBTWP XJHZWNYD
  Decrypted  : NETWORK SECURITY
  Enc. Time  : 0.0021 ms
  Dec. Time  : 0.0019 ms
```

> "Caesar cipher with shift 5 — note how spaces are preserved 
> and the decryption perfectly recovers the original."

**Press Enter** to return to menu.

---

## SCENE 4 — Hill Cipher & Matrix Display (1:25–1:55)

**Type:** `4`

**Type plaintext:** `ACT`

**Type key:** `6,24,1,13,16,10,20,17,15`

**Expected:**
```
  Key Matrix:
      6   24    1
     13   16   10
     20   17   15

  Inverse Key Matrix (mod 26):
      8    5   10
     21    8   21
     21   12    8

  Plaintext  : ACT
  Ciphertext : POH
  Decrypted  : ACT
```

> "Hill cipher using a 3×3 matrix. Notice the key matrix and its 
> modular inverse (mod 26) are displayed. The classic ACT → POH vector."

**Press Enter.**

---

## SCENE 5 — Compare Algorithms (1:55–2:35)

**Type:** `9`

**Type plaintext:** `CRYPTOGRAPHY`

**Expected:** Table comparing all 8 ciphers showing:
- Algorithm name, type, key, ciphertext
- Encryption and decryption times
- Round-trip verification (Yes/No)
- Strength notes

> "Option 9 runs all eight ciphers on the same plaintext and displays 
> a comparison table with timing. You can see the OTP is the strongest — 
> perfect secrecy when used correctly."

**Press Enter.**

---

## SCENE 6 — Encrypt a Text File (2:35–3:00)

**Type:** `10`

**Type path:** `samples/sample_plain.txt`

**Select cipher:** `1` (Caesar)

**Type key:** `13`

**Expected:**
```
  Loaded 743 characters from 'samples/sample_plain.txt'
  Cipher    : Caesar
  Enc. Time : 0.0412 ms
  Output    : samples/sample_plain_encrypted.txt
```

> "Option 10 lets you encrypt any text file. The output is saved 
> automatically with an `_encrypted` suffix."

**Press Enter.**

---

## SCENE 7 — Run All Tests (3:00–3:20)

**[Open a second terminal]**

**Type:**
```
python tests/test_ciphers.py
```

**Expected (last lines):**
```
Ran 76 tests in 0.016s
OK
```

> "The toolkit has 76 automated unit tests covering round-trip correctness, 
> known vectors, invalid keys, edge cases, and space preservation. All pass."

---

## SCENE 8 — Launch the GUI (3:20–4:15)

**Type:**
```
python main.py --gui
```

**[Tkinter window opens with dark theme]**

> "The GUI provides the same functionality visually."

**Demo steps in GUI:**
1. Select **"1. Caesar Cipher"** from dropdown.
2. Type `HELLO WORLD` in the Plaintext box.
3. Type `5` in the Key field.
4. Click **🔒 Encrypt** → output appears, time shown.
5. Click **🔓 Decrypt** → original text restored.
6. Select **"2. Monoalphabetic Cipher"**.
7. Click **🎲 Generate Random Key** → 26-letter key auto-filled.
8. Click the **Compare** tab.
9. Type `NETWORK` and click **▶ Run All Ciphers**.
10. Table appears showing all 8 results.

> "The Generate Random Key button works for Monoalphabetic and OTP ciphers. 
> You can also load files and save output from the GUI."

---

## SCENE 9 — Wrap-Up (4:15–4:45)

**[Screen: Project folder tree]**

> "To summarise — this toolkit includes:
> - 8 classical ciphers: Caesar, Monoalphabetic, Playfair, Hill, Vigenère, 
>   One-Time Pad, Rail Fence, and Columnar Transposition
> - A menu-driven CLI with password protection
> - A Tkinter GUI with dark theme
> - File-level encryption and decryption
> - Algorithm comparison with timing
> - 76 unit tests — all passing
> - Full documentation including a project report and user manual
>
> This project was built for the Network Security course, Final Year ECM 2026-27.
> Thank you!"

---

## Input Cheat Sheet (for recording)

| Scene | Input |
|-------|-------|
| Password | `crypto2026` |
| Caesar | Plain=`NETWORK SECURITY`, Key=`5` |
| Hill | Plain=`ACT`, Key=`6,24,1,13,16,10,20,17,15` |
| Compare | Plain=`CRYPTOGRAPHY` |
| File enc | Path=`samples/sample_plain.txt`, cipher=`1`, key=`13` |
| Test run | `python tests/test_ciphers.py` |
| GUI | Plain=`HELLO WORLD`, Key=`5` (Caesar) |
