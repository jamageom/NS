"""
Rail Fence Cipher (Transposition)
====================================
Characters are written diagonally across *n* rails in a zig-zag pattern,
then read row by row to produce the ciphertext.

Example (3 rails, plaintext "WEAREDISCOVEREDFLEEAMONOW"):
    Rail 0: W . . . E . . . I . . . V . . . D . . . E . . .
    Rail 1: . E . R . D . S . O . E . E . F . E . A . O . O .
    Rail 2: . . A . . . C . . . R . . . L . . . N . . . W . .
    Ciphertext: WEIVDE + ERDSOEEFEEAOO + ACRLNW

Decryption: reconstruct the zig-zag pattern and read off letters.
"""


class RailFenceCipher:
    """Implements the Rail Fence (zig-zag) transposition cipher."""

    NAME = "Rail Fence Cipher"
    TYPE = "Transposition"

    @staticmethod
    def _validate_rails(rails: int) -> None:
        """
        Ensure the number of rails is valid.

        Args:
            rails: Must be an integer ≥ 2.

        Raises:
            ValueError: If rails < 2 or not an integer.
        """
        if not isinstance(rails, int) or rails < 2:
            raise ValueError(f"Number of rails must be an integer ≥ 2 (got {rails!r}).")

    def get_zig_zag_grid(self, text: str, rails: int) -> str:
        """Return a printable zig-zag grid for visualisation."""
        n = len(text)
        grid = [['.' for _ in range(n)] for _ in range(rails)]
        rail, direction = 0, 1
        for col, ch in enumerate(text):
            grid[rail][col] = ch
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        lines = [f"  Rail {r}: " + " ".join(grid[r]) for r in range(rails)]
        return "\n".join(lines)

    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Encrypt *plaintext* using the Rail Fence cipher.

        Args:
            plaintext: Message to encrypt (spaces and punctuation included).
            key: Number of rails (integer ≥ 2).

        Returns:
            Ciphertext (same characters, reordered).

        Example:
            >>> RailFenceCipher().encrypt("WEAREDISCOVERED", 3)
            'WECRLTEERDSOEIA'
        """
        rails = int(key)
        self._validate_rails(rails)

        fence: list[list[str]] = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for ch in plaintext:
            fence[rail].append(ch)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        return "".join("".join(r) for r in fence)

    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Decrypt *ciphertext* using the Rail Fence cipher.

        Args:
            ciphertext: Encrypted message.
            key: Number of rails used during encryption.

        Returns:
            Original plaintext.
        """
        rails = int(key)
        self._validate_rails(rails)
        n = len(ciphertext)

        # Compute rail lengths
        pattern = self._get_rail_pattern(n, rails)
        counts = [0] * rails
        for r in pattern:
            counts[r] += 1

        # Slice ciphertext into rails
        fence: list[list[str]] = []
        idx = 0
        for r in range(rails):
            fence.append(list(ciphertext[idx:idx + counts[r]]))
            idx += counts[r]

        # Read off zig-zag order
        result: list[str] = []
        rail_idx = [0] * rails
        for r in pattern:
            result.append(fence[r][rail_idx[r]])
            rail_idx[r] += 1
        return "".join(result)

    @staticmethod
    def _get_rail_pattern(n: int, rails: int) -> list[int]:
        """Return the sequence of rail indices for *n* characters on *rails* rails."""
        pattern: list[int] = []
        rail, direction = 0, 1
        for _ in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return pattern
