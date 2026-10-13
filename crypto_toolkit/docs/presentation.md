# Presentation Slides — Classical Cryptography Toolkit
## Network Security | Final Year ECM 2026-27

---

## SLIDE 1 — Title Slide

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         CLASSICAL CRYPTOGRAPHY TOOLKIT                       ║
║         ─────────────────────────────────                    ║
║         Network Security Mini Project                        ║
║                                                              ║
║         Name    : [YOUR NAME]                                ║
║         Roll No.: [ROLL]                                     ║
║         Batch   : [BATCH]                                    ║
║         Class   : Final Year ECM 2026-27                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Key visual:** Padlock icon, binary/hex background pattern.

---

## SLIDE 2 — Problem Statement & Objectives

### Problem Statement
> Classical cryptography forms the foundation of modern security.
> This project builds a complete, interactive Python toolkit implementing
> eight classical ciphers to bridge theory and hands-on practice in
> Network Security.

### Objectives
✅ Implement 8 classical ciphers (4 substitution + 4... err 2 transposition)  
✅ Provide CLI + Tkinter GUI  
✅ Enable text file encryption/decryption  
✅ Compare algorithms on security strength & performance  
✅ 76 automated unit tests — all passing  

---

## SLIDE 3 — System Design & Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Entry Points                       │
│   main.py (CLI)              gui.py (Tkinter GUI)    │
└──────────────────┬──────────────────────────────────┘
                   │
       ┌───────────▼────────────┐
       │      ciphers/          │
       │  caesar.py             │
       │  monoalphabetic.py     │
       │  playfair.py           │
       │  hill.py               │
       │  vigenere.py           │
       │  otp.py                │
       │  railfence.py          │
       │  columnar.py           │
       └───────────┬────────────┘
                   │
       ┌───────────▼────────────┐
       │       utils/           │
       │  file_ops.py           │
       │  timing.py             │
       │  validators.py         │
       └────────────────────────┘
```

### Key Design Decisions
- Each cipher = one file, `encrypt()` + `decrypt()` interface
- Validators centralised — no duplication
- `time.perf_counter` for microsecond-level timing

---

## SLIDE 4 — The 8 Algorithms

| # | Cipher | Type | Key | Strength |
|---|--------|------|-----|----------|
| 1 | **Caesar** | Substitution | Integer shift | ⭐ (25 keys) |
| 2 | **Monoalphabetic** | Substitution | 26-letter perm | ⭐⭐ (26! keys) |
| 3 | **Playfair** | Substitution | Keyword (5×5) | ⭐⭐⭐ |
| 4 | **Hill** | Substitution | Matrix (2×2/3×3) | ⭐⭐⭐ |
| 5 | **Vigenère** | Polyalphabetic | Keyword | ⭐⭐⭐ |
| 6 | **One-Time Pad** | Substitution | Random key | ⭐⭐⭐⭐⭐ (perfect) |
| 7 | **Rail Fence** | Transposition | No. of rails | ⭐ |
| 8 | **Columnar** | Transposition | Keyword | ⭐⭐ |

### Mandatory Test Case (Caesar, key=5):
```
Input:  NETWORK SECURITY
Output: SJYBTWP XJHZWNYD  ✓
```

---

## SLIDE 5 — Demo & Results

### CLI Demo
```
Enter your Choice : 1          ← Caesar Cipher
  Enter Plaintext : NETWORK SECURITY
  Enter Key       : 5

  Plaintext  : NETWORK SECURITY
  Ciphertext : SJYBTWP XJHZWNYD
  Decrypted  : NETWORK SECURITY
  Enc. Time  : 0.0021 ms
  Dec. Time  : 0.0019 ms
```

### Test Results
```
Ran 76 tests in 0.016s
OK  ← 76/76 pass
```

### Algorithm Comparison (sample)
| Algorithm | Enc Time | Dec Time | Round-trip |
|-----------|----------|----------|------------|
| Caesar | 0.002 ms | 0.002 ms | ✅ Yes |
| OTP | 0.003 ms | 0.003 ms | ✅ Yes |
| Hill | 0.015 ms | 0.018 ms | ✅ Yes |
| Playfair | 0.012 ms | 0.011 ms | ✅ Yes |

---

## SLIDE 6 — Conclusion & Future Scope

### Conclusion
- **Built and tested** 8 complete classical ciphers in Python
- **76 unit tests**, all passing — round-trip, vectors, edge cases
- **Password-protected** CLI with SHA-256 hash
- **Tkinter GUI** with dark theme, file I/O, compare tab
- **Timing analysis** for every operation

### What We Learned
- Modular Python architecture (packages, imports, OOP)
- Cryptographic principles: substitution vs. transposition
- Why classical ciphers fail (key space, frequency analysis)
- How to unit test cryptographic code

### Future Scope
🔒 Add **AES-256 / RSA** modules  
🌐 Port to **Flask web app**  
📊 Add **cryptanalysis** (frequency analysis, Kasiski test)  
📱 Build **Android/iOS** app using Kivy  
🎬 Visual **animations** in GUI (matrix operations, zig-zag)  

---

*Classical Cryptography Toolkit — Presentation — Final Year ECM 2026-27*
