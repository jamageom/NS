"""
Caesar Cipher
=============
Shift each alphabetic character by a fixed integer key (mod 26).
Spaces, punctuation, and digits are preserved unchanged.
Output is always uppercase.

Formula:
    Encrypt: C = (P - 65 + key) mod 26 + 65   (for uppercase letters)
    Decrypt: P = (C - 65 - key) mod 26 + 65
"""


class CaesarCipher:
    """Implements the Caesar (shift) cipher."""

    NAME = "Caesar Cipher"
    TYPE = "Substitution"

    @staticmethod
    def _validate_key(key: int) -> int:
        """Validate and normalise the key to [0, 25]."""
        if not isinstance(key, int):
            raise ValueError("Caesar key must be an integer.")
        return key % 26

    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Encrypt *plaintext* with a Caesar shift of *key*.

        Args:
            plaintext: The message to encrypt (any case).
            key: Integer shift value (reduced mod 26 internally).

        Returns:
            Uppercase ciphertext with non-alpha characters preserved.

        Example:
            >>> CaesarCipher().encrypt("NETWORK SECURITY", 5)
            'SJYBTWP XJHZWNYD'
        """
        shift = self._validate_key(key)
        result: list[str] = []
        for ch in plaintext.upper():
            if ch.isalpha():
                encrypted = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
                result.append(encrypted)
            else:
                result.append(ch)  # preserve spaces, digits, punctuation
        return "".join(result)

    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Decrypt *ciphertext* using a Caesar shift of *key*.

        Args:
            ciphertext: The encrypted message (any case).
            key: Integer shift value used during encryption.

        Returns:
            Uppercase plaintext with non-alpha characters preserved.

        Example:
            >>> CaesarCipher().decrypt("SJYBTWP XJHZWNYD", 5)
            'NETWORK SECURITY'
        """
        shift = self._validate_key(key)
        return self.encrypt(ciphertext, -shift)
