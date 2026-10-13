"""
Timing Utility
===============
Provides a context manager and helper function to measure execution time
using time.perf_counter for high-resolution timing.
"""

import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def measure_time() -> Generator[dict, None, None]:
    """
    Context manager that records elapsed wall-clock time.

    Usage::

        with measure_time() as t:
            result = cipher.encrypt(text, key)
        print(f"Took {t['elapsed']:.6f} seconds")
    """
    data: dict = {}
    start = time.perf_counter()
    try:
        yield data
    finally:
        data['elapsed'] = time.perf_counter() - start


def time_operation(func, *args, **kwargs) -> tuple:
    """
    Execute *func* with *args*/*kwargs* and return (result, elapsed_seconds).

    Args:
        func: Callable to time.
        *args: Positional arguments for *func*.
        **kwargs: Keyword arguments for *func*.

    Returns:
        Tuple of (return_value, elapsed_time_in_seconds).
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def format_time(seconds: float) -> str:
    """
    Format *seconds* into a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        String like '1.234 ms' or '0.001 μs'.
    """
    if seconds >= 1:
        return f"{seconds:.4f} s"
    elif seconds >= 1e-3:
        return f"{seconds * 1e3:.4f} ms"
    elif seconds >= 1e-6:
        return f"{seconds * 1e6:.4f} μs"
    else:
        return f"{seconds * 1e9:.4f} ns"
