"""
Playfair Cipher
================
A digraph substitution cipher using a 5x5 key matrix (I and J are merged).

Key construction:
    1. Remove duplicate letters from the keyword.
    2. Append remaining letters of the alphabet (I/J merged).
    3. Fill a 5x5 matrix row by row.

Digraph rules:
    - Same row   → shift right (wrap).
    - Same column → shift down (wrap).
    - Rectangle  → swap columns.

Plaintext preparation:
    - Uppercase, remove non-alpha, merge I/J.
    - Insert 'X' between repeated letters in a pair.
    - Pad with 'X' if odd length.

Decryption reverses the shifts.
"""


class PlayfairCipher:
    """Implements the Playfair cipher."""

    NAME = "Playfair Cipher"
    TYPE = "Substitution"

    def _build_matrix(self, keyword: str) -> list[list[str]]:
        """
        Build the 5x5 Playfair matrix from *keyword*.

        Args:
            keyword: The key word/phrase (letters only; case-insensitive).

        Returns:
            5x5 list of lists of characters.
        """
        keyword = keyword.upper().replace('J', 'I')
        seen: set[str] = set()
        order: list[str] = []
        for ch in keyword:
            if ch.isalpha() and ch not in seen:
                seen.add(ch)
                order.append(ch)
        for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # no J
            if ch not in seen:
                seen.add(ch)
                order.append(ch)
        matrix = [order[i * 5:(i + 1) * 5] for i in range(5)]
        return matrix

    def _get_position(self, matrix: list[list[str]], ch: str) -> tuple[int, int]:
        """Return (row, col) of *ch* in *matrix*."""
        for r, row in enumerate(matrix):
            if ch in row:
                return r, row.index(ch)
        raise ValueError(f"Character '{ch}' not found in Playfair matrix.")

    def _prepare_plaintext(self, plaintext: str) -> str:
        """
        Prepare plaintext for Playfair encryption.

        Converts to uppercase, removes non-alpha, replaces J with I,
        inserts 'X' between repeated letters in a pair, pads to even length.
        """
        text = plaintext.upper().replace('J', 'I')
        text = ''.join(ch for ch in text if ch.isalpha())

        # Insert 'X' between repeated characters in a digraph
        prepared: list[str] = []
        i = 0
        while i < len(text):
            prepared.append(text[i])
            if i + 1 < len(text) and text[i] == text[i + 1]:
                prepared.append('X')
            i += 1

        if len(prepared) % 2 != 0:
            prepared.append('X')
        return "".join(prepared)

    def _process_digraph(self, matrix: list[list[str]], a: str, b: str, mode: str) -> str:
        """
        Encrypt or decrypt a single digraph (*a*, *b*).

        Args:
            mode: 'encrypt' shifts right/down; 'decrypt' shifts left/up.
        """
        r1, c1 = self._get_position(matrix, a)
        r2, c2 = self._get_position(matrix, b)
        shift = 1 if mode == 'encrypt' else -1

        if r1 == r2:  # Same row → shift columns
            return matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:  # Same column → shift rows
            return matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
        else:  # Rectangle → swap columns
            return matrix[r1][c2] + matrix[r2][c1]

    def get_matrix_str(self, keyword: str) -> str:
        """Return a formatted string representation of the 5x5 matrix."""
        matrix = self._build_matrix(keyword)
        lines = ["  Playfair Matrix:"]
        for row in matrix:
            lines.append("  " + " ".join(row))
        return "\n".join(lines)

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt *plaintext* using the Playfair cipher.

        Args:
            plaintext: Message to encrypt.
            key: Keyword for building the 5x5 matrix.

        Returns:
            Uppercase ciphertext (may include padding 'X').

        Example:
            >>> PlayfairCipher().encrypt("HELLO WORLD", "KEYWORD")
            'DCKISZRBUI'
        """
        if not key.strip():
            raise ValueError("Playfair key cannot be empty.")
        matrix = self._build_matrix(key)
        prepared = self._prepare_plaintext(plaintext)
        result: list[str] = []
        for i in range(0, len(prepared), 2):
            result.append(self._process_digraph(matrix, prepared[i], prepared[i + 1], 'encrypt'))
        return "".join(result)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt *ciphertext* using the Playfair cipher.

        Args:
            ciphertext: Encrypted message (letters only, even length).
            key: Keyword used during encryption.

        Returns:
            Uppercase plaintext (may contain padding 'X').
        """
        if not key.strip():
            raise ValueError("Playfair key cannot be empty.")
        matrix = self._build_matrix(key)
        text = ciphertext.upper().replace('J', 'I')
        text = ''.join(ch for ch in text if ch.isalpha())
        if len(text) % 2 != 0:
            raise ValueError("Playfair ciphertext length must be even.")
        result: list[str] = []
        for i in range(0, len(text), 2):
            result.append(self._process_digraph(matrix, text[i], text[i + 1], 'decrypt'))
        return "".join(result)
