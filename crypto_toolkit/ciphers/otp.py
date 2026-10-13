"""
One-Time Pad (OTP)
===================
A theoretically unbreakable cipher when used correctly.

Rules (enforced):
    1. Key must be at least as long as the plaintext alphabet characters.
    2. Key must be truly random (auto-generation provided).
    3. Key must NEVER be reused (a warning is issued if the same key is
       used in the same session).

Formula:
    Encrypt: C_i = (P_i + K_i) mod 26
    Decrypt: P_i = (C_i - K_i) mod 26
    (only letter positions consume key characters; spaces preserved)
"""

import random
import string


class OneTimePad:
    """Implements the One-Time Pad cipher."""

    NAME = "One-Time Pad"
    TYPE = "Substitution"

    _used_keys: set[str] = set()  # track used keys within a session

    @classmethod
    def generate_key(cls, plaintext: str) -> str:
        """
        Generate a random OTP key long enough for *plaintext*.

        Args:
            plaintext: The plaintext to be encrypted.

        Returns:
            Uppercase random key string of length = number of alpha chars
            in plaintext (or at least 1).
        """
        alpha_count = max(1, sum(1 for ch in plaintext if ch.isalpha()))
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(alpha_count))
        return key

    @classmethod
    def _validate_key(cls, plaintext: str, key: str) -> str:
        """
        Validate the OTP key.

        Args:
            plaintext: Original plaintext (used to count alpha chars).
            key: Must be alphabetic and long enough.

        Returns:
            Uppercase key.

        Raises:
            ValueError: If key is too short or contains non-letters.
        """
        key = key.upper().strip()
        if not key.isalpha():
            raise ValueError("OTP key must contain only letters (A-Z).")
        alpha_count = sum(1 for ch in plaintext if ch.isalpha())
        if len(key) < alpha_count:
            raise ValueError(
                f"OTP key is too short: need at least {alpha_count} letters "
                f"for this plaintext (got {len(key)})."
            )
        return key

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt *plaintext* using the One-Time Pad.

        Args:
            plaintext: Message to encrypt.
            key: Random key ≥ len(alpha chars in plaintext).

        Returns:
            Uppercase ciphertext; non-alpha characters preserved.

        Example:
            >>> otp = OneTimePad()
            >>> key = otp.generate_key("HELLO")
            >>> cipher = otp.encrypt("HELLO", key)
            >>> otp.decrypt(cipher, key)
            'HELLO'
        """
        key = self._validate_key(plaintext, key)

        # Warn if key has been used before
        if key in self._used_keys:
            print(
                "\n  ⚠️  WARNING: This OTP key has been used before in this session! "
                "Reusing keys compromises OTP security."
            )
        self._used_keys.add(key)

        result: list[str] = []
        k_idx = 0
        for ch in plaintext.upper():
            if ch.isalpha():
                shift = ord(key[k_idx]) - ord('A')
                result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
                k_idx += 1
            else:
                result.append(ch)
        return "".join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt *ciphertext* using the One-Time Pad.

        Args:
            ciphertext: Encrypted message.
            key: Exact key used during encryption.

        Returns:
            Uppercase plaintext; non-alpha characters preserved.
        """
        key = self._validate_key(ciphertext, key)
        result: list[str] = []
        k_idx = 0
        for ch in ciphertext.upper():
            if ch.isalpha():
                shift = ord(key[k_idx]) - ord('A')
                result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
                k_idx += 1
            else:
                result.append(ch)
        return "".join(result)
