"""
Validators Utility
===================
Centralised validation helpers for user inputs.
"""

import math
import re


def validate_non_empty(text: str, field_name: str = "Input") -> str:
    """Raise ValueError if *text* is empty after stripping."""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return text.strip()


def validate_integer(value: str, field_name: str = "Key") -> int:
    """
    Parse *value* as an integer.

    Raises:
        ValueError: If *value* is not a valid integer string.
    """
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        raise ValueError(f"{field_name} must be an integer (got '{value}').")


def validate_rails(value: str) -> int:
    """Parse and validate number of rails (must be integer ≥ 2)."""
    n = validate_integer(value, "Number of rails")
    if n < 2:
        raise ValueError(f"Number of rails must be ≥ 2 (got {n}).")
    return n


def validate_alpha_key(key: str, field_name: str = "Key") -> str:
    """Validate that *key* is a non-empty alphabetic string."""
    key = validate_non_empty(key, field_name).upper()
    if not key.isalpha():
        raise ValueError(f"{field_name} must contain only letters A-Z.")
    return key


def validate_mono_key(key: str) -> str:
    """Validate a 26-letter monoalphabetic key."""
    key = key.upper().strip()
    if len(key) != 26:
        raise ValueError(f"Monoalphabetic key must be exactly 26 letters (got {len(key)}).")
    if not key.isalpha():
        raise ValueError("Monoalphabetic key must contain only letters A-Z.")
    if len(set(key)) != 26:
        raise ValueError("Monoalphabetic key must have all 26 unique letters.")
    return key


def validate_hill_matrix_string(value: str) -> list[list[int]]:
    """
    Parse a comma-separated Hill matrix string.

    Accepted: "3,7,2,5" (2×2) or "6,24,1,13,16,10,20,17,15" (3×3)

    Returns:
        n×n list of ints.

    Raises:
        ValueError: If format is invalid or not 2×2/3×3.
    """
    try:
        values = [int(v.strip()) for v in value.split(',')]
    except ValueError:
        raise ValueError("Hill key must be comma-separated integers, e.g. '3,7,2,5'.")
    n = int(len(values) ** 0.5)
    if n * n != len(values) or n not in (2, 3):
        raise ValueError(
            f"Hill key must have 4 values (2×2) or 9 values (3×3); got {len(values)}."
        )
    return [values[i * n:(i + 1) * n] for i in range(n)]


def validate_otp_key(plaintext: str, key: str) -> str:
    """Validate an OTP key against *plaintext*."""
    key = key.upper().strip()
    if not key.isalpha():
        raise ValueError("OTP key must contain only letters A-Z.")
    alpha_count = sum(1 for ch in plaintext if ch.isalpha())
    if len(key) < alpha_count:
        raise ValueError(
            f"OTP key too short: need ≥ {alpha_count} letters, got {len(key)}."
        )
    return key


def validate_file_path(path: str) -> str:
    """Strip and return *path* after checking it is not empty."""
    path = path.strip()
    if not path:
        raise ValueError("File path cannot be empty.")
    return path
