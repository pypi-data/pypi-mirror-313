from typing import Self

__all__ = ["sum_as_string", "TimeSeries"]


class TimeSeries:

    def __init__(self, index: list[int], values: list[float]) -> None:
        """Create a new timeseries."""

    def __new__(self, index: list[int], values: list[float]) -> Self: ...

    def sma(self, windows_size: int) -> list[float]:
        """Calculate simple moving average."""


def sum_as_string(a: int, b: int) -> str:
    """Calculates the sum of two numbers and return the result as string.

    Args:
        a: A number.
        b: Another number.

    Returns:
        Sum of a and b.
    """
