"""
Classical Cryptography Toolkit — Tkinter GUI
=============================================
Launch with:  python main.py --gui

Features:
  • Dropdown for all 8 ciphers
  • Plaintext / ciphertext text boxes
  • Key field with "Generate Random Key" button (where applicable)
  • Encrypt / Decrypt buttons with execution-time label
  • Load File / Save Output buttons
  • Compare tab showing all ciphers on one plaintext
  • Clean, readable layout
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os
import time

# Allow running standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers import (
    CaesarCipher, MonoalphabeticCipher, PlayfairCipher,
    HillCipher, VigenereCipher, OneTimePad,
    RailFenceCipher, ColumnarCipher,
)
from utils.timing import format_time, time_operation
from utils.file_ops import load_text_file, save_text_file, get_output_path
from utils.validators import (
    validate_non_empty, validate_integer, validate_rails,
    validate_alpha_key, validate_mono_key, validate_hill_matrix_string,
)

# ── Cipher registry ──────────────────────────────────────
_CIPHERS = {
    "1. Caesar Cipher":               CaesarCipher(),
    "2. Monoalphabetic Cipher":       MonoalphabeticCipher(),
    "3. Playfair Cipher":             PlayfairCipher(),
    "4. Hill Cipher":                 HillCipher(),
    "5. Vigenère Cipher":             VigenereCipher(),
    "6. One-Time Pad":                OneTimePad(),
    "7. Rail Fence Cipher":           RailFenceCipher(),
    "8. Columnar Transposition":      ColumnarCipher(),
}

_KEY_HINTS = {
    "1. Caesar Cipher":          "Integer shift, e.g. 5",
    "2. Monoalphabetic Cipher":  "26 unique letters, e.g. QWERTYUIOPASDFGHJKLZXCVBNM",
    "3. Playfair Cipher":        "Keyword, e.g. KEYWORD",
    "4. Hill Cipher":            "Comma-separated ints: 3,7,2,5 (2×2) or 9 ints (3×3)",
    "5. Vigenère Cipher":        "Alphabetic keyword, e.g. KEY",
    "6. One-Time Pad":           "Random letters ≥ plaintext length",
    "7. Rail Fence Cipher":      "Number of rails (integer ≥ 2)",
    "8. Columnar Transposition": "Keyword, e.g. ZEBRA",
}

_RANDOM_KEY_CIPHERS = {"2. Monoalphabetic Cipher", "6. One-Time Pad"}


def _parse_key(cipher_name: str, key_str: str, plaintext: str = "") -> object:
    """Parse key string into the correct type for the selected cipher."""
    if cipher_name == "1. Caesar Cipher":
        return validate_integer(key_str, "Caesar key")
    elif cipher_name == "2. Monoalphabetic Cipher":
        return validate_mono_key(key_str)
    elif cipher_name in ("3. Playfair Cipher", "5. Vigenère Cipher", "8. Columnar Transposition"):
        return validate_alpha_key(key_str)
    elif cipher_name == "4. Hill Cipher":
        return validate_hill_matrix_string(key_str)
    elif cipher_name == "6. One-Time Pad":
        return key_str.upper().strip()
    elif cipher_name == "7. Rail Fence Cipher":
        return validate_rails(key_str)
    else:
        return key_str


def _generate_random_key(cipher_name: str, plaintext: str = "") -> str:
    """Return a randomly generated key string for ciphers that support it."""
    if cipher_name == "2. Monoalphabetic Cipher":
        return MonoalphabeticCipher.generate_key()
    elif cipher_name == "6. One-Time Pad":
        return OneTimePad.generate_key(plaintext or "A" * 16)
    return ""


# ── Main Application Window ───────────────────────────────


class CryptoToolkitApp(tk.Tk):
    """Root Tkinter application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Classical Cryptography Toolkit  |  Network Security 2026-27")
        self.geometry("950x700")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        self._build_style()
        self._build_notebook()

    # ── Styling ──────────────────────────────────────────

    def _build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        bg   = "#1e1e2e"
        fg   = "#cdd6f4"
        acc  = "#89b4fa"
        btn  = "#313244"
        ebtn = "#a6e3a1"
        dbtn = "#f38ba8"

        style.configure("TNotebook",        background=bg, borderwidth=0)
        style.configure("TNotebook.Tab",    background=btn, foreground=fg,
                        padding=[14, 6], font=("Consolas", 10, "bold"))
        style.map("TNotebook.Tab",          background=[("selected", acc)],
                  foreground=[("selected", "#1e1e2e")])
        style.configure("TFrame",           background=bg)
        style.configure("TLabel",           background=bg, foreground=fg, font=("Consolas", 10))
        style.configure("TCombobox",        fieldbackground=btn, foreground=fg,
                        background=btn, selectbackground=acc)
        style.configure("Encrypt.TButton", background=ebtn, foreground="#1e1e2e",
                        font=("Consolas", 10, "bold"), padding=[8, 4])
        style.configure("Decrypt.TButton", background=dbtn, foreground="#1e1e2e",
                        font=("Consolas", 10, "bold"), padding=[8, 4])
        style.configure("TButton",          background=btn, foreground=fg,
                        font=("Consolas", 10), padding=[8, 4])
        style.map("TButton",               background=[("active", acc)],
                  foreground=[("active", "#1e1e2e")])

        self._colors = {"bg": bg, "fg": fg, "acc": acc, "btn": btn,
                        "entry_bg": "#313244", "entry_fg": fg}

    def _text_widget(self, parent, height: int = 6, **kw) -> scrolledtext.ScrolledText:
        c = self._colors
        w = scrolledtext.ScrolledText(
            parent, height=height, wrap=tk.WORD,
            font=("Consolas", 10),
            bg=c["entry_bg"], fg=c["entry_fg"],
            insertbackground=c["fg"],
            relief="flat", bd=4,
            **kw
        )
        return w

    def _label(self, parent, text: str, bold: bool = False) -> ttk.Label:
        font = ("Consolas", 10, "bold") if bold else ("Consolas", 10)
        lbl = ttk.Label(parent, text=text, font=font)
        return lbl

    def _entry(self, parent, width: int = 40) -> ttk.Entry:
        c = self._colors
        e = tk.Entry(parent, width=width,
                     bg=c["entry_bg"], fg=c["entry_fg"],
                     insertbackground=c["fg"],
                     relief="flat", bd=4,
                     font=("Consolas", 10))
        return e

    # ── Notebook / Tabs ──────────────────────────────────

    def _build_notebook(self) -> None:
        self._nb = ttk.Notebook(self)
        self._nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._main_tab = ttk.Frame(self._nb)
        self._compare_tab = ttk.Frame(self._nb)

        self._nb.add(self._main_tab,    text="  🔐 Cipher  ")
        self._nb.add(self._compare_tab, text="  📊 Compare  ")

        self._build_main_tab()
        self._build_compare_tab()

    # ── Main Cipher Tab ──────────────────────────────────

    def _build_main_tab(self) -> None:
        tab = self._main_tab
        c   = self._colors

        # ── Row 0: Cipher selector ──
        row0 = ttk.Frame(tab)
        row0.pack(fill=tk.X, padx=16, pady=(12, 4))
        self._label(row0, "Select Cipher:", bold=True).pack(side=tk.LEFT, padx=(0, 8))

        self._cipher_var = tk.StringVar(value=list(_CIPHERS.keys())[0])
        self._cipher_combo = ttk.Combobox(row0, textvariable=self._cipher_var,
                                          values=list(_CIPHERS.keys()),
                                          state="readonly", width=36,
                                          font=("Consolas", 10))
        self._cipher_combo.pack(side=tk.LEFT)
        self._cipher_combo.bind("<<ComboboxSelected>>", self._on_cipher_change)

        # ── Row 1: Plaintext ──
        row1 = ttk.Frame(tab)
        row1.pack(fill=tk.X, padx=16, pady=(8, 0))
        self._label(row1, "Plaintext:", bold=True).pack(anchor=tk.W)

        btn_row1 = ttk.Frame(tab)
        btn_row1.pack(fill=tk.X, padx=16)
        ttk.Button(btn_row1, text="📂 Load File", command=self._load_file).pack(side=tk.LEFT, padx=(0, 6))

        self._plain_box = self._text_widget(tab, height=5)
        self._plain_box.pack(fill=tk.X, padx=16, pady=(2, 6))

        # ── Row 2: Key ──
        key_frame = ttk.Frame(tab)
        key_frame.pack(fill=tk.X, padx=16, pady=4)
        self._label(key_frame, "Key:", bold=True).pack(side=tk.LEFT, padx=(0, 8))

        self._key_entry = self._entry(key_frame, width=40)
        self._key_entry.pack(side=tk.LEFT, padx=(0, 8))

        self._gen_key_btn = ttk.Button(key_frame, text="🎲 Generate Random Key",
                                       command=self._generate_key)
        self._gen_key_btn.pack(side=tk.LEFT)

        self._key_hint_var = tk.StringVar()
        ttk.Label(tab, textvariable=self._key_hint_var,
                  font=("Consolas", 9), foreground="#6c7086",
                  background=c["bg"]).pack(anchor=tk.W, padx=16)

        # ── Row 3: Action buttons ──
        btn_row = ttk.Frame(tab)
        btn_row.pack(fill=tk.X, padx=16, pady=8)
        ttk.Button(btn_row, text="🔒 Encrypt", style="Encrypt.TButton",
                   command=self._do_encrypt).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row, text="🔓 Decrypt", style="Decrypt.TButton",
                   command=self._do_decrypt).pack(side=tk.LEFT, padx=(0, 20))

        self._time_var = tk.StringVar(value="")
        ttk.Label(btn_row, textvariable=self._time_var,
                  font=("Consolas", 9), foreground="#a6e3a1",
                  background=c["bg"]).pack(side=tk.LEFT)

        # ── Row 4: Ciphertext output ──
        ttk.Frame(tab).pack(fill=tk.X, padx=16, pady=(4, 0))
        self._label(tab, "Ciphertext / Output:", bold=True).pack(anchor=tk.W, padx=16)

        self._cipher_box = self._text_widget(tab, height=5)
        self._cipher_box.pack(fill=tk.BOTH, expand=True, padx=16, pady=(2, 4))

        # ── Row 5: Save / Clear ──
        row5 = ttk.Frame(tab)
        row5.pack(fill=tk.X, padx=16, pady=(0, 10))
        ttk.Button(row5, text="💾 Save Output", command=self._save_output).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(row5, text="🗑 Clear All",    command=self._clear_all).pack(side=tk.LEFT)

        # Initialise state
        self._on_cipher_change()

    def _on_cipher_change(self, _event=None) -> None:
        name = self._cipher_var.get()
        self._key_hint_var.set("  Key format: " + _KEY_HINTS.get(name, ""))
        can_gen = name in _RANDOM_KEY_CIPHERS
        self._gen_key_btn.configure(state="normal" if can_gen else "disabled")

    def _generate_key(self) -> None:
        name = self._cipher_var.get()
        plain = self._plain_box.get("1.0", tk.END).strip()
        key  = _generate_random_key(name, plain)
        self._key_entry.delete(0, tk.END)
        self._key_entry.insert(0, key)

    def _load_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            try:
                content = load_text_file(path)
                self._plain_box.delete("1.0", tk.END)
                self._plain_box.insert("1.0", content)
                self._last_input_path = path
            except Exception as ex:
                messagebox.showerror("Load Error", str(ex))

    def _save_output(self) -> None:
        content = self._cipher_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to save", "Output box is empty.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            try:
                save_text_file(path, content)
                messagebox.showinfo("Saved", f"Output saved to:\n{path}")
            except Exception as ex:
                messagebox.showerror("Save Error", str(ex))

    def _clear_all(self) -> None:
        self._plain_box.delete("1.0", tk.END)
        self._cipher_box.delete("1.0", tk.END)
        self._key_entry.delete(0, tk.END)
        self._time_var.set("")

    def _do_encrypt(self) -> None:
        self._run_cipher(mode="encrypt")

    def _do_decrypt(self) -> None:
        self._run_cipher(mode="decrypt")

    def _run_cipher(self, mode: str) -> None:
        name    = self._cipher_var.get()
        cipher  = _CIPHERS[name]
        key_str = self._key_entry.get().strip()
        text    = self._plain_box.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Input required", "Please enter text in the Plaintext box.")
            return
        if not key_str:
            messagebox.showwarning("Key required", "Please enter (or generate) a key.")
            return

        try:
            key = _parse_key(name, key_str, text)
            fn  = cipher.encrypt if mode == "encrypt" else cipher.decrypt
            result, elapsed = time_operation(fn, text, key)

            self._cipher_box.delete("1.0", tk.END)
            self._cipher_box.insert("1.0", result)
            self._time_var.set(f"⏱ {mode.capitalize()} time: {format_time(elapsed)}")
        except Exception as ex:
            messagebox.showerror(f"{mode.capitalize()} Error", str(ex))

    # ── Compare Tab ──────────────────────────────────────

    def _build_compare_tab(self) -> None:
        tab = self._compare_tab
        c   = self._colors

        top = ttk.Frame(tab)
        top.pack(fill=tk.X, padx=16, pady=12)
        self._label(top, "Plaintext for comparison:", bold=True).pack(side=tk.LEFT, padx=(0, 8))
        self._cmp_plain_entry = self._entry(top, width=40)
        self._cmp_plain_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(top, text="▶ Run All Ciphers", command=self._run_compare).pack(side=tk.LEFT)

        self._cmp_result = self._text_widget(tab, height=30)
        self._cmp_result.pack(fill=tk.BOTH, expand=True, padx=16, pady=(4, 12))

    def _run_compare(self) -> None:
        text = self._cmp_plain_entry.get().strip()
        if not text:
            messagebox.showwarning("Input required", "Enter a plaintext to compare.")
            return

        otp_key = OneTimePad.generate_key(text)
        hill_matrix = [[3, 7], [2, 5]]  # valid 2x2

        configs = [
            ("Caesar",    "Substitution",  CaesarCipher(),         3),
            ("Mono",      "Substitution",  MonoalphabeticCipher(),  MonoalphabeticCipher.generate_key()),
            ("Playfair",  "Substitution",  PlayfairCipher(),        "KEYWORD"),
            ("Hill",      "Substitution",  HillCipher(),            hill_matrix),
            ("Vigenère",  "Substitution",  VigenereCipher(),        "KEY"),
            ("OTP",       "Substitution",  OneTimePad(),            otp_key),
            ("RailFence", "Transposition", RailFenceCipher(),       3),
            ("Columnar",  "Transposition", ColumnarCipher(),        "ZEBRA"),
        ]

        lines = [
            "=" * 90,
            f"  {'Algorithm':<14} {'Type':<14} {'Key':<20} {'Ciphertext':<24} {'Enc':<10} {'Dec':<10} {'OK?'}",
            "=" * 90,
        ]

        for name, typ, cipher, key in configs:
            try:
                ct, et = time_operation(cipher.encrypt, text, key)
                pt, dt = time_operation(cipher.decrypt, ct, key)
                orig  = ''.join(ch for ch in text.upper() if ch.isalpha())
                got   = ''.join(ch for ch in pt.upper() if ch.isalpha())
                ok    = "✓ Yes" if got.startswith(orig) else "✗ No"
                ks    = str(key)[:18] + ("…" if len(str(key)) > 18 else "")
                cs    = ct[:22] + ("…" if len(ct) > 22 else "")
                lines.append(f"  {name:<14} {typ:<14} {ks:<20} {cs:<24} {format_time(et):<10} {format_time(dt):<10} {ok}")
            except Exception as ex:
                lines.append(f"  {name:<14} {typ:<14} {'(error)':<20} {str(ex)[:24]:<24} {'N/A':<10} {'N/A':<10} ✗ No")

        lines += [
            "=" * 90,
            "",
            "Strength Notes:",
            "  Caesar      : Key space = 25. Trivially brute-forced.",
            "  Mono        : Key space ≈ 26! ≈ 4×10²⁶. Broken by frequency analysis.",
            "  Playfair    : Digraph cipher; harder to break with short texts.",
            "  Hill        : Matrix cipher; vulnerable to known-plaintext attack.",
            "  Vigenère    : Key space = 26^|key|. Broken by Kasiski examination.",
            "  OTP         : Perfect secrecy when key is truly random and never reused.",
            "  Rail Fence  : Very weak; brute-forceable.",
            "  Columnar    : Moderate; broken by anagramming columns.",
        ]

        self._cmp_result.delete("1.0", tk.END)
        self._cmp_result.insert("1.0", "\n".join(lines))


# ── Launch ────────────────────────────────────────────────


def launch() -> None:
    """Create and run the Tkinter application."""
    app = CryptoToolkitApp()
    app.mainloop()


if __name__ == "__main__":
    launch()
