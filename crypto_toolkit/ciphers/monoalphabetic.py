"""
Monoalphabetic Substitution Cipher
====================================
Each letter of the alphabet is replaced by a unique substitute letter
defined by a 26-character key string (a permutation of A-Z).

Key format  : 26 unique uppercase letters, e.g. "QWERTYUIOPASDFGHJKLZXCVBNM"
              Maps A→Q, B→W, C→E, … Z→M

Formula:
    Encrypt: C = key[P - 65]
    Decrypt: P = inverse_key[C - 65]   (reverse the mapping)
"""

import random
import string


class MonoalphabeticCipher:
    """Implements the Monoalphabetic Substitution cipher."""

    NAME = "Monoalphabetic Cipher"
    TYPE = "Substitution"

    @staticmethod
    def generate_key() -> str:
        """
        Generate a random 26-letter substitution key.

        Returns:
            A shuffled uppercase alphabet string of length 26.
        """
        alphabet = list(string.ascii_uppercase)
        random.shuffle(alphabet)
        return "".join(alphabet)

    @staticmethod
    def _validate_key(key: str) -> str:
        """
        Validate the substitution key.

        Args:
            key: Must be exactly 26 unique uppercase letters.

        Returns:
            Normalised uppercase key.

        Raises:
            ValueError: If key length ≠ 26 or contains duplicates/non-letters.
        """
        key = key.upper().strip()
        if len(key) != 26:
            raise ValueError(f"Monoalphabetic key must be exactly 26 letters (got {len(key)}).")
        if not key.isalpha():
            raise ValueError("Monoalphabetic key must contain only letters.")
        if len(set(key)) != 26:
            raise ValueError("Monoalphabetic key must have 26 unique letters (no repeats).")
        return key

    def _build_inverse(self, key: str) -> str:
        """Build the inverse substitution mapping for decryption."""
        inverse = [''] * 26
        for i, ch in enumerate(key):
            inverse[ord(ch) - ord('A')] = chr(i + ord('A'))
        return "".join(inverse)

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt *plaintext* using monoalphabetic substitution.

        Args:
            plaintext: Message to encrypt (any case).
            key: 26-letter substitution alphabet.

        Returns:
            Uppercase ciphertext; non-alpha characters preserved.

        Example:
            >>> MonoalphabeticCipher().encrypt("HELLO", "QWERTYUIOPASDFGHJKLZXCVBNM")
            'ITSSG'
        """
        key = self._validate_key(key)
        result: list[str] = []
        for ch in plaintext.upper():
            if ch.isalpha():
                result.append(key[ord(ch) - ord('A')])
            else:
                result.append(ch)
        return "".join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt *ciphertext* using the inverse monoalphabetic mapping.

        Args:
            ciphertext: Encrypted message.
            key: 26-letter substitution alphabet used for encryption.

        Returns:
            Uppercase plaintext; non-alpha characters preserved.
        """
        key = self._validate_key(key)
        inv = self._build_inverse(key)
        result: list[str] = []
        for ch in ciphertext.upper():
            if ch.isalpha():
                result.append(inv[ord(ch) - ord('A')])
            else:
                result.append(ch)
        return "".join(result)
