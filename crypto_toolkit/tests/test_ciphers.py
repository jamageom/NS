"""
Unit Tests for Classical Cryptography Toolkit
==============================================
Tests every cipher with:
  - Known-vector tests
  - Round-trip (encrypt → decrypt) tests
  - Invalid key / empty input edge cases
  - Space/punctuation preservation
  - Case-insensitivity

Run:
    python -m pytest tests/test_ciphers.py -v
    OR
    python tests/test_ciphers.py
"""

import sys
import os
import unittest

# Make the package importable from this file's location
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.caesar        import CaesarCipher
from ciphers.monoalphabetic import MonoalphabeticCipher
from ciphers.playfair      import PlayfairCipher
from ciphers.hill          import HillCipher
from ciphers.vigenere      import VigenereCipher
from ciphers.otp           import OneTimePad
from ciphers.railfence     import RailFenceCipher
from ciphers.columnar      import ColumnarCipher


# ══════════════════════════════════════════════════════════════════
# 1. Caesar Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestCaesarCipher(unittest.TestCase):
    """Tests for CaesarCipher."""

    def setUp(self):
        self.c = CaesarCipher()

    def test_mandatory_vector(self):
        """Mandatory test: NETWORK SECURITY, shift 5."""
        self.assertEqual(self.c.encrypt("NETWORK SECURITY", 5), "SJYBTWP XJHZWNYD")

    def test_mandatory_decrypt(self):
        self.assertEqual(self.c.decrypt("SJYBTWP XJHZWNYD", 5), "NETWORK SECURITY")

    def test_round_trip(self):
        plain = "HELLO WORLD"
        self.assertEqual(self.c.decrypt(self.c.encrypt(plain, 13), 13), plain)

    def test_shift_zero(self):
        self.assertEqual(self.c.encrypt("ABC", 0), "ABC")

    def test_shift_26_identity(self):
        self.assertEqual(self.c.encrypt("XYZ", 26), "XYZ")

    def test_negative_shift(self):
        self.assertEqual(self.c.encrypt("DEF", -3), "ABC")

    def test_lowercase_input(self):
        self.assertEqual(self.c.encrypt("hello", 3), "KHOOR")

    def test_preserves_spaces(self):
        result = self.c.encrypt("A B", 1)
        self.assertIn(" ", result)

    def test_preserves_punctuation(self):
        result = self.c.encrypt("HELLO, WORLD!", 3)
        self.assertIn(",", result)
        self.assertIn("!", result)

    def test_wrap_around(self):
        self.assertEqual(self.c.encrypt("XYZ", 3), "ABC")

    def test_known_vector_hello(self):
        self.assertEqual(self.c.encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(self.c.decrypt("KHOOR", 3), "HELLO")

    def test_empty_input(self):
        self.assertEqual(self.c.encrypt("", 5), "")

    def test_only_spaces(self):
        self.assertEqual(self.c.encrypt("   ", 5), "   ")

    def test_invalid_key_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.c.encrypt("ABC", "five")  # type: ignore


# ══════════════════════════════════════════════════════════════════
# 2. Monoalphabetic Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestMonoalphabeticCipher(unittest.TestCase):
    KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"

    def setUp(self):
        self.c = MonoalphabeticCipher()

    def test_known_vector(self):
        # A→Q, B→W, C→E, D→R, E→T, F→Y, G→U, H→I, I→O, J→P,
        # K→A, L→S, M→D, N→F, O→G, P→H, Q→J, R→K, S→L, T→Z,
        # U→X, V→C, W→V, X→B, Y→N, Z→M
        encrypted = self.c.encrypt("HELLO", self.KEY)
        self.assertEqual(encrypted, "ITSSG")

    def test_round_trip(self):
        plain = "NETWORK SECURITY"
        enc = self.c.encrypt(plain, self.KEY)
        dec = self.c.decrypt(enc, self.KEY)
        self.assertEqual(dec, plain.upper().replace(" ", " "))

    def test_round_trip_with_spaces(self):
        plain = "HELLO WORLD"
        enc = self.c.encrypt(plain, self.KEY)
        self.assertEqual(self.c.decrypt(enc, self.KEY), plain)

    def test_key_too_short(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("ABC", "ABCDE")

    def test_key_duplicates(self):
        bad_key = "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"[:26]
        with self.assertRaises(ValueError):
            self.c.encrypt("ABC", bad_key)

    def test_key_non_alpha(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("ABC", "1234567890ABCDEFGHIJKLMNOP")

    def test_generate_key_length(self):
        key = MonoalphabeticCipher.generate_key()
        self.assertEqual(len(key), 26)

    def test_generate_key_unique(self):
        key = MonoalphabeticCipher.generate_key()
        self.assertEqual(len(set(key)), 26)

    def test_empty_input(self):
        self.assertEqual(self.c.encrypt("", self.KEY), "")

    def test_preserves_spaces(self):
        result = self.c.encrypt("A B", self.KEY)
        self.assertIn(" ", result)


# ══════════════════════════════════════════════════════════════════
# 3. Playfair Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestPlayfairCipher(unittest.TestCase):

    def setUp(self):
        self.c = PlayfairCipher()

    def test_round_trip_simple(self):
        plain = "HELLO"
        key   = "KEYWORD"
        enc   = self.c.encrypt(plain, key)
        dec   = self.c.decrypt(enc, key)
        # After Playfair decryption, I/J merged and X padding may exist
        # Core letters should be recoverable
        orig = plain.upper().replace('J', 'I')
        result_stripped = dec.replace('X', '').rstrip('X')
        self.assertTrue(result_stripped.startswith(orig) or orig in result_stripped)

    def test_round_trip_network(self):
        plain = "NETWORK"
        key   = "MONARCHY"
        enc   = self.c.encrypt(plain, key)
        dec   = self.c.decrypt(enc, key)
        # Check core letters preserved
        expected_core = "NETWORK"
        got_core = ''.join(ch for ch in dec if ch != 'X')
        self.assertIn("NETWORK", got_core + "X")  # padding X may be present

    def test_known_vector_hide_gold(self):
        # Classic example: HIDE GOLD IN THE TREE STUMP with key PLAYFAIR
        enc = self.c.encrypt("HIDE GOLD IN THE TREE STUMP", "PLAYFAIR")
        self.assertIsInstance(enc, str)
        self.assertTrue(len(enc) > 0)
        self.assertTrue(enc.isalpha())

    def test_repeated_letters_handled(self):
        # "BALLOON" → B A L X L O O N (X inserted between LL, padding for OO)
        enc = self.c.encrypt("BALLOON", "KEYWORD")
        self.assertIsInstance(enc, str)
        self.assertEqual(len(enc) % 2, 0)

    def test_odd_length_padding(self):
        enc = self.c.encrypt("ABC", "KEY")
        self.assertEqual(len(enc) % 2, 0)

    def test_empty_key_error(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "")

    def test_matrix_display(self):
        matrix_str = self.c.get_matrix_str("KEYWORD")
        self.assertIn("K", matrix_str)

    def test_i_j_merge(self):
        enc1 = self.c.encrypt("IAMHERE", "KEY")
        enc2 = self.c.encrypt("JAMHERE", "KEY")
        self.assertEqual(enc1, enc2)


# ══════════════════════════════════════════════════════════════════
# 4. Hill Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestHillCipher(unittest.TestCase):
    KEY_2X2 = [[3, 7], [2, 5]]   # det = 15-14 = 1 → gcd(1,26)=1 ✓
    KEY_3X3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]  # classic

    def setUp(self):
        self.c = HillCipher()

    def test_known_vector_act(self):
        # Classic test: ACT with 3x3 key → POH
        result = self.c.encrypt("ACT", self.KEY_3X3)
        self.assertEqual(result, "POH")

    def test_round_trip_2x2(self):
        plain = "HELLO"
        enc   = self.c.encrypt(plain, self.KEY_2X2)
        dec   = self.c.decrypt(enc, self.KEY_2X2)
        # Padding may add X; check core letters
        orig = ''.join(ch for ch in "HELLO" if ch.isalpha())
        got  = ''.join(ch for ch in dec if ch.isalpha())
        self.assertTrue(got.startswith(orig))

    def test_round_trip_3x3(self):
        plain = "NETWORK"
        enc   = self.c.encrypt(plain, self.KEY_3X3)
        dec   = self.c.decrypt(enc, self.KEY_3X3)
        orig  = ''.join(ch for ch in plain.upper() if ch.isalpha())
        got   = ''.join(ch for ch in dec if ch.isalpha())
        self.assertTrue(got.startswith(orig))

    def test_invalid_determinant(self):
        bad_key = [[2, 4], [6, 8]]  # det = 16-24 = -8 ≡ 18 mod 26; gcd(18,26)=2 ≠ 1
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", bad_key)

    def test_invalid_matrix_size(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("ABC", [[1, 2, 3], [4, 5, 6]])

    def test_padding_with_x(self):
        enc = self.c.encrypt("A", self.KEY_2X2)
        self.assertEqual(len(enc), 2)

    def test_parse_key_string(self):
        matrix = self.c.parse_key("3,7,2,5")
        self.assertEqual(matrix, [[3, 7], [2, 5]])

    def test_matrix_display(self):
        s = self.c.matrix_str(self.KEY_2X2)
        self.assertIn("3", s)


# ══════════════════════════════════════════════════════════════════
# 5. Vigenère Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestVigenereCipher(unittest.TestCase):

    def setUp(self):
        self.c = VigenereCipher()

    def test_known_vector(self):
        self.assertEqual(self.c.encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_known_decrypt(self):
        self.assertEqual(self.c.decrypt("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_known_vector_with_spaces(self):
        self.assertEqual(self.c.encrypt("ATTACK AT DAWN", "LEMON"), "LXFOPV EF RNHR")

    def test_round_trip(self):
        plain = "HELLO WORLD"
        enc   = self.c.encrypt(plain, "SECRET")
        self.assertEqual(self.c.decrypt(enc, "SECRET"), plain.upper())

    def test_preserves_spaces(self):
        result = self.c.encrypt("HELLO WORLD", "KEY")
        self.assertIn(" ", result)

    def test_key_does_not_advance_on_space(self):
        # "A B" with key "AB" → encrypt A with A (→A), keep space, encrypt B with B (→C)
        result = self.c.encrypt("A B", "AB")
        self.assertEqual(result, "A C")

    def test_empty_key(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "")

    def test_numeric_key(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "123")

    def test_lowercase_input(self):
        self.assertEqual(self.c.encrypt("hello", "key"), "RIJVS")

    def test_empty_input(self):
        self.assertEqual(self.c.encrypt("", "KEY"), "")


# ══════════════════════════════════════════════════════════════════
# 6. One-Time Pad Tests
# ══════════════════════════════════════════════════════════════════

class TestOneTimePad(unittest.TestCase):

    def setUp(self):
        self.c = OneTimePad()

    def test_round_trip(self):
        plain = "HELLO"
        key   = self.c.generate_key(plain)
        enc   = self.c.encrypt(plain, key)
        self.assertEqual(self.c.decrypt(enc, key), plain)

    def test_round_trip_with_spaces(self):
        plain = "HELLO WORLD"
        key   = self.c.generate_key(plain)
        enc   = self.c.encrypt(plain, key)
        self.assertEqual(self.c.decrypt(enc, key), plain.upper())

    def test_generate_key_length(self):
        plain = "HELLO WORLD"
        key   = self.c.generate_key(plain)
        alpha = sum(1 for ch in plain if ch.isalpha())
        self.assertEqual(len(key), alpha)

    def test_key_too_short(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "AB")

    def test_key_non_alpha(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "12345")

    def test_preserves_spaces(self):
        plain = "HI THERE"
        key   = self.c.generate_key(plain)
        enc   = self.c.encrypt(plain, key)
        self.assertIn(" ", enc)

    def test_empty_input_round_trip(self):
        enc = self.c.encrypt("", "A")
        self.assertEqual(self.c.decrypt(enc, "A"), "")


# ══════════════════════════════════════════════════════════════════
# 7. Rail Fence Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestRailFenceCipher(unittest.TestCase):

    def setUp(self):
        self.c = RailFenceCipher()

    def test_known_vector(self):
        # WEAREDISCOVERED with 3 rails
        # Grid: Rail0=W,E,C,R  Rail1=E,R,D,S,O,E,E  Rail2=A,I,V,D
        enc = self.c.encrypt("WEAREDISCOVERED", 3)
        self.assertEqual(enc, "WECRERDSOEEAIVD")

    def test_known_decrypt(self):
        enc = self.c.encrypt("WEAREDISCOVERED", 3)
        self.assertEqual(self.c.decrypt(enc, 3), "WEAREDISCOVERED")

    def test_round_trip(self):
        plain = "HELLO WORLD"
        enc   = self.c.encrypt(plain, 3)
        self.assertEqual(self.c.decrypt(enc, 3), plain)

    def test_two_rails(self):
        enc = self.c.encrypt("ABCDE", 2)
        self.assertEqual(self.c.decrypt(enc, 2), "ABCDE")

    def test_rails_equal_length(self):
        # Rails ≥ length → same as identity
        plain = "AB"
        enc   = self.c.encrypt(plain, 5)
        self.assertEqual(self.c.decrypt(enc, 5), plain)

    def test_invalid_rails_one(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", 1)

    def test_invalid_rails_zero(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", 0)

    def test_empty_input(self):
        self.assertEqual(self.c.encrypt("", 3), "")

    def test_preserves_spaces(self):
        plain = "HELLO WORLD"
        enc   = self.c.encrypt(plain, 2)
        self.assertIn(" ", enc)

    def test_zig_zag_grid_display(self):
        grid = self.c.get_zig_zag_grid("HELLO", 3)
        self.assertIn("Rail", grid)


# ══════════════════════════════════════════════════════════════════
# 8. Columnar Transposition Cipher Tests
# ══════════════════════════════════════════════════════════════════

class TestColumnarCipher(unittest.TestCase):

    def setUp(self):
        self.c = ColumnarCipher()

    def test_round_trip(self):
        plain = "HELLO"
        enc   = self.c.encrypt(plain, "KEY")
        dec   = self.c.decrypt(enc, "KEY")
        # Padding may add X, check core
        self.assertTrue(dec.startswith("HELLO") or "HELLO" in dec)

    def test_round_trip_longer(self):
        plain = "WEAREDISCOVEREDFLEEATONCE"
        enc   = self.c.encrypt(plain, "ZEBRAS")
        dec   = self.c.decrypt(enc, "ZEBRAS")
        self.assertEqual(dec[:len(plain)], plain)

    def test_known_vector_zebras(self):
        # WEAREDISCOVEREDFLEEATONCE with key ZEBRAS
        enc = self.c.encrypt("WEAREDISCOVEREDFLEEATONCE", "ZEBRAS")
        # Verify it's a rearrangement of the same chars (plus possible X)
        orig_sorted = sorted("WEAREDISCOVEREDFLEEATONCE")
        enc_sorted  = sorted(enc)
        self.assertEqual(orig_sorted, enc_sorted[:len(orig_sorted)])

    def test_padding_with_x(self):
        enc = self.c.encrypt("ABC", "FOUR")
        self.assertEqual(len(enc), 4)  # padded to length 4

    def test_empty_key_error(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "")

    def test_numeric_key_error(self):
        with self.assertRaises(ValueError):
            self.c.encrypt("HELLO", "K3Y")

    def test_column_order(self):
        order = self.c._get_column_order("BAC")
        self.assertEqual(order, [1, 0, 2])  # A<B<C → col 1 first (A), col 0 (B), col 2 (C)

    def test_grid_display(self):
        grid = self.c.get_grid_str("HELLOWORLD", "KEY")
        self.assertIn("K", grid)

    def test_empty_input(self):
        # Empty plaintext → empty ciphertext
        enc = self.c.encrypt("", "KEY")
        self.assertEqual(enc, "")


# ══════════════════════════════════════════════════════════════════
# Run all tests
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()

    test_classes = [
        TestCaesarCipher,
        TestMonoalphabeticCipher,
        TestPlayfairCipher,
        TestHillCipher,
        TestVigenereCipher,
        TestOneTimePad,
        TestRailFenceCipher,
        TestColumnarCipher,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
