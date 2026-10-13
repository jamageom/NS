"""
Vigenère (Polyalphabetic) Cipher
==================================
Uses a repeating keyword to shift each letter by different amounts.
Non-letter characters are preserved without advancing the key index.

Formula:
    Encrypt: C_i = (P_i + K_{i mod m}) mod 26
    Decrypt: P_i = (C_i - K_{i mod m}) mod 26
    where K_j = ord(keyword[j]) - 65
"""


class VigenereCipher:
    """Implements the Vigenère polyalphabetic cipher."""

    NAME = "Vigenère Cipher"
    TYPE = "Substitution"

    @staticmethod
    def _validate_key(key: str) -> str:
        """
        Validate the Vigenère keyword.

        Args:
            key: Must be a non-empty alphabetic string.

        Returns:
            Uppercase keyword.

        Raises:
            ValueError: If key is empty or contains non-letter characters.
        """
        key = key.upper().strip()
        if not key:
            raise ValueError("Vigenère key cannot be empty.")
        if not key.isalpha():
            raise ValueError("Vigenère key must contain only letters (A-Z).")
        return key

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt *plaintext* using the Vigenère cipher.

        Args:
            plaintext: Message to encrypt (any case).
            key: Alphabetic keyword (repeats as needed).

        Returns:
            Uppercase ciphertext; non-alpha characters unchanged.

        Example:
            >>> VigenereCipher().encrypt("ATTACK AT DAWN", "LEMON")
            'LXFOPV EF RNHR'
        """
        key = self._validate_key(key)
        result: list[str] = []
        k_idx = 0
        for ch in plaintext.upper():
            if ch.isalpha():
                shift = ord(key[k_idx % len(key)]) - ord('A')
                encrypted = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
                result.append(encrypted)
                k_idx += 1
            else:
                result.append(ch)  # preserve, don't advance key
        return "".join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt *ciphertext* using the Vigenère cipher.

        Args:
            ciphertext: Encrypted message (any case).
            key: Alphabetic keyword used during encryption.

        Returns:
            Uppercase plaintext; non-alpha characters unchanged.

        Example:
            >>> VigenereCipher().decrypt("LXFOPV EF RNHR", "LEMON")
            'ATTACK AT DAWN'
        """
        key = self._validate_key(key)
        result: list[str] = []
        k_idx = 0
        for ch in ciphertext.upper():
            if ch.isalpha():
                shift = ord(key[k_idx % len(key)]) - ord('A')
                decrypted = chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
                result.append(decrypted)
                k_idx += 1
            else:
                result.append(ch)
        return "".join(result)
