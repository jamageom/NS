"""
Hill Cipher
============
A polygraphic cipher using linear algebra over Z_26.

Supports 2x2 and 3x3 key matrices.

Formula (n×n blocks):
    Encrypt: C = (K × P) mod 26
    Decrypt: P = (K⁻¹ × C) mod 26

Requirements:
    - Key matrix must be invertible mod 26, i.e. gcd(det(K), 26) = 1.
    - Plaintext is padded with 'X' to a multiple of n.
"""

import math
from typing import Union


Matrix = list[list[int]]


class HillCipher:
    """Implements the Hill cipher for 2x2 and 3x3 key matrices."""

    NAME = "Hill Cipher"
    TYPE = "Substitution"

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _det2(m: Matrix) -> int:
        """Determinant of a 2x2 matrix."""
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    @staticmethod
    def _det3(m: Matrix) -> int:
        """Determinant of a 3x3 matrix (cofactor expansion)."""
        return (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )

    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        """Extended Euclidean algorithm to find modular inverse of *a* mod *m*."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError(f"No modular inverse for {a} mod {m}.")

    def _validate_matrix(self, matrix: Matrix) -> int:
        """
        Validate the key matrix and return its size (2 or 3).

        Raises:
            ValueError: If matrix is not 2×2 or 3×3, or not invertible mod 26.
        """
        n = len(matrix)
        if n not in (2, 3):
            raise ValueError("Hill cipher supports only 2x2 or 3x3 matrices.")
        for row in matrix:
            if len(row) != n:
                raise ValueError(f"Key matrix must be {n}x{n}.")
            for val in row:
                if not isinstance(val, int):
                    raise ValueError("Key matrix values must be integers.")

        det = self._det2(matrix) if n == 2 else self._det3(matrix)
        det_mod = det % 26
        if math.gcd(det_mod, 26) != 1:
            raise ValueError(
                f"Key matrix determinant ({det} ≡ {det_mod} mod 26) is not "
                f"invertible mod 26 (gcd={math.gcd(det_mod, 26)}). "
                "Choose a different key matrix."
            )
        return n

    def _adjugate2(self, m: Matrix) -> Matrix:
        """Adjugate (classical adjoint) of a 2x2 matrix."""
        return [[m[1][1], -m[0][1]], [-m[1][0], m[0][0]]]

    def _adjugate3(self, m: Matrix) -> Matrix:
        """Adjugate of a 3x3 matrix (transpose of cofactor matrix)."""
        cof = [[0] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                # 2x2 minor
                minor = [
                    [m[i][j] for j in range(3) if j != c]
                    for i in range(3) if i != r
                ]
                cof[r][c] = ((-1) ** (r + c)) * self._det2(minor)
        # Transpose
        adj = [[cof[j][i] for j in range(3)] for i in range(3)]
        return adj

    def _mat_inverse_mod26(self, matrix: Matrix, n: int) -> Matrix:
        """Compute the modular inverse of *matrix* mod 26."""
        det = self._det2(matrix) if n == 2 else self._det3(matrix)
        det_inv = self._mod_inverse(det % 26, 26)
        adj = self._adjugate2(matrix) if n == 2 else self._adjugate3(matrix)
        inv = [[(det_inv * adj[r][c]) % 26 for c in range(n)] for r in range(n)]
        return inv

    def _mat_vec_mul_mod26(self, matrix: Matrix, vec: list[int]) -> list[int]:
        """Multiply a matrix by a column vector mod 26."""
        n = len(matrix)
        result = [0] * n
        for r in range(n):
            for c in range(n):
                result[r] += matrix[r][c] * vec[c]
            result[r] %= 26
        return result

    # ------------------------------------------------------------------ public

    def matrix_str(self, matrix: Matrix) -> str:
        """Return a printable string of the key matrix."""
        lines = ["  Key Matrix:"]
        for row in matrix:
            lines.append("  " + "  ".join(f"{v:3d}" for v in row))
        return "\n".join(lines)

    def parse_key(self, key_input: Union[str, list]) -> Matrix:
        """
        Parse a key from a flat comma-separated string or nested list.

        Accepted formats:
            "3,7,2,5"      → 2×2 matrix
            "6,24,1,13,16,10,20,17,15"  → 3×3 matrix
        """
        if isinstance(key_input, list):
            return key_input
        values = [int(v.strip()) for v in str(key_input).split(',')]
        n = int(len(values) ** 0.5)
        if n * n != len(values):
            raise ValueError(
                "Hill key must have 4 values (2x2) or 9 values (3x3), "
                f"got {len(values)}."
            )
        return [values[i * n:(i + 1) * n] for i in range(n)]

    def encrypt(self, plaintext: str, key: Union[str, Matrix]) -> str:
        """
        Encrypt *plaintext* using the Hill cipher.

        Args:
            plaintext: Message to encrypt.
            key: Comma-separated string or n×n list of ints.

        Returns:
            Uppercase ciphertext (padded with 'X' to a multiple of n).

        Example:
            >>> HillCipher().encrypt("ACT", [[6,24,1],[13,16,10],[20,17,15]])
            'POH'
        """
        matrix = self.parse_key(key)
        n = self._validate_matrix(matrix)

        text = ''.join(ch for ch in plaintext.upper() if ch.isalpha())
        # Pad with 'X'
        while len(text) % n != 0:
            text += 'X'

        result: list[str] = []
        for i in range(0, len(text), n):
            block = [ord(text[i + j]) - ord('A') for j in range(n)]
            enc = self._mat_vec_mul_mod26(matrix, block)
            result.extend(chr(v + ord('A')) for v in enc)
        return "".join(result)

    def decrypt(self, ciphertext: str, key: Union[str, Matrix]) -> str:
        """
        Decrypt *ciphertext* using the Hill cipher.

        Args:
            ciphertext: Encrypted message.
            key: Same key matrix used for encryption.

        Returns:
            Uppercase plaintext (trailing padding 'X' may remain).
        """
        matrix = self.parse_key(key)
        n = self._validate_matrix(matrix)
        inv_matrix = self._mat_inverse_mod26(matrix, n)

        text = ''.join(ch for ch in ciphertext.upper() if ch.isalpha())
        if len(text) % n != 0:
            raise ValueError(f"Ciphertext length must be a multiple of {n} for Hill decryption.")

        result: list[str] = []
        for i in range(0, len(text), n):
            block = [ord(text[i + j]) - ord('A') for j in range(n)]
            dec = self._mat_vec_mul_mod26(inv_matrix, block)
            result.extend(chr(v + ord('A')) for v in dec)
        return "".join(result)

    def get_inverse_str(self, key: Union[str, Matrix]) -> str:
        """Return the modular inverse matrix as a formatted string."""
        matrix = self.parse_key(key)
        n = self._validate_matrix(matrix)
        inv = self._mat_inverse_mod26(matrix, n)
        lines = ["  Inverse Key Matrix (mod 26):"]
        for row in inv:
            lines.append("  " + "  ".join(f"{v:3d}" for v in row))
        return "\n".join(lines)
