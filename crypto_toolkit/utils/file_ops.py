"""
File Operations Utility
========================
Provides functions to load and save text files for encryption/decryption.
"""

import os


def load_text_file(filepath: str) -> str:
    """
    Read and return the contents of a text file.

    Args:
        filepath: Absolute or relative path to the file.

    Returns:
        File contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be read.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def save_text_file(filepath: str, content: str) -> str:
    """
    Write *content* to *filepath*, creating directories as needed.

    Args:
        filepath: Destination file path.
        content: Text to write.

    Returns:
        Absolute path of the saved file.

    Raises:
        IOError: If the file cannot be written.
    """
    dirpath = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(dirpath, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return os.path.abspath(filepath)


def get_output_path(input_path: str, suffix: str) -> str:
    """
    Generate an output file path by inserting *suffix* before the extension.

    Args:
        input_path: Original file path.
        suffix: E.g. '_encrypted' or '_decrypted'.

    Returns:
        New file path string.

    Example:
        >>> get_output_path("samples/plain.txt", "_encrypted")
        'samples/plain_encrypted.txt'
    """
    base, ext = os.path.splitext(input_path)
    return base + suffix + (ext if ext else '.txt')
