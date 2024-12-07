
__all__ = ["Maximum", "Minimum",
           "SimpleMovingAverage",  "sum_as_string"]


class Maximum:

    def __init__(self, period: int) -> None:
        """Create a new maximum indicator."""

    def period(self) -> int:
        """Return the number of periods."""

    def next(self, input: float) -> float:
        """Calculate the maximum of the current periods."""

    def reset(self) -> None:
        """Reset the current calculations."""


class Minimum:

    def __init__(self, period: int) -> None:
        """Create a minimum indicator."""

    def period(self) -> int:
        """Return the number of periods."""

    def next(self, input: float) -> float:
        """Calculate the minimm of the current periods."""

    def reset(self) -> None:
        """Reset the current calculations."""


class SimpleMovingAverage:

    def __init__(self, period: int) -> None:
        """Create a simple moving average indicator."""

    def period(self) -> int:
        """Return the number of periods."""

    def next(self, input: float) -> float:
        """Calculate the simple moving average of the current periods."""

    def reset(self) -> None:
        """Reset the current calculations."""


def sum_as_string(a: int, b: int) -> str:
    """Calculates the sum of two numbers and return the result as string.

    Args:
        a: A number.
        b: Another number.

    Returns:
        Sum of a and b.
    """
