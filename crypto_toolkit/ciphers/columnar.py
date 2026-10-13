"""
Columnar Transposition Cipher
================================
Plaintext is written in rows of width = len(keyword).
Columns are read in the alphabetical order of the keyword letters.

Key format: Any word/phrase (letters only), e.g. "ZEBRAS"
            Determines column order by sorting letters alphabetically.

Padding: 'X' is appended if plaintext length is not a multiple of key length.
"""


class ColumnarCipher:
    """Implements the Columnar Transposition cipher."""

    NAME = "Columnar Transposition Cipher"
    TYPE = "Transposition"

    @staticmethod
    def _validate_key(key: str) -> str:
        """
        Validate the columnar transposition key.

        Args:
            key: Must be a non-empty alphabetic string.

        Returns:
            Uppercase key.

        Raises:
            ValueError: If key is empty or contains non-letter characters.
        """
        key = key.upper().strip()
        if not key:
            raise ValueError("Columnar Transposition key cannot be empty.")
        if not key.isalpha():
            raise ValueError("Columnar Transposition key must contain only letters.")
        return key

    @staticmethod
    def _get_column_order(key: str) -> list[int]:
        """
        Compute the column reading order from *key*.

        Returns a list of column indices sorted by their key character
        (alphabetically). Ties broken by position (left-to-right).

        Example:
            key = "ZEBRAS" → order = [3, 0, 4, 2, 1, 5] (B,E,R,S,Z -> column indices)
        """
        indexed = sorted(enumerate(key), key=lambda x: (x[1], x[0]))
        return [col for col, _ in indexed]

    def get_grid_str(self, text: str, key: str) -> str:
        """Return a printable string showing the columnar grid."""
        key = self._validate_key(key)
        ncols = len(key)
        rows = [text[i:i + ncols] for i in range(0, len(text), ncols)]
        lines = ["  Key: " + "  ".join(key)]
        lines.append("  " + "-" * (ncols * 3))
        for row in rows:
            lines.append("  " + "  ".join(row))
        order = self._get_column_order(key)
        lines.append("  Read order: " + " → ".join(str(o) for o in order))
        return "\n".join(lines)

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt *plaintext* using Columnar Transposition.

        Args:
            plaintext: Message to encrypt.
            key: Keyword determining column order.

        Returns:
            Uppercase ciphertext (padded with 'X' if needed).

        Example:
            >>> ColumnarCipher().encrypt("WEAREDISCOVEREDFLEEATONCE", "ZEBRAS")
            'EVLNE ACDTEB EMOHSS FODRIE'  # (approximately, spaces stripped)
        """
        key = self._validate_key(key)
        ncols = len(key)
        text = plaintext.upper()

        # Pad with 'X'
        while len(text) % ncols != 0:
            text += 'X'

        # Build grid (rows × cols)
        grid: list[list[str]] = []
        for i in range(0, len(text), ncols):
            grid.append(list(text[i:i + ncols]))

        # Read columns in alphabetical key order
        order = self._get_column_order(key)
        result: list[str] = []
        for col in order:
            for row in grid:
                result.append(row[col])
        return "".join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt *ciphertext* using Columnar Transposition.

        Args:
            ciphertext: Encrypted message.
            key: Same keyword used during encryption.

        Returns:
            Uppercase plaintext (may contain trailing 'X' padding).
        """
        key = self._validate_key(key)
        ncols = len(key)
        text = ciphertext.upper()

        if len(text) % ncols != 0:
            raise ValueError(
                f"Columnar ciphertext length ({len(text)}) is not a multiple "
                f"of key length ({ncols})."
            )

        nrows = len(text) // ncols
        order = self._get_column_order(key)

        # Determine which original column each position maps to
        inv_order = [0] * ncols
        for rank, col in enumerate(order):
            inv_order[col] = rank

        # Slice ciphertext into columns
        columns: dict[int, list[str]] = {}
        idx = 0
        for rank, col in enumerate(order):
            columns[col] = list(text[idx:idx + nrows])
            idx += nrows

        # Read off row by row
        result: list[str] = []
        for r in range(nrows):
            for c in range(ncols):
                result.append(columns[c][r])
        return "".join(result)
