r"""Implement trackers to track the moving average value of float
number."""

from __future__ import annotations

__all__ = ["ExponentialMovingAverage", "MovingAverage"]

from collections import deque
from typing import TYPE_CHECKING, Any

import torch

from karbonn.utils.tracker.exception import EmptyTrackerError

try:
    from typing import Self  # Introduced in python 3.11
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Iterable


class MovingAverage:
    r"""Implement a tracker to track the moving average value of float
    number.

    Args:
        values: The initial values.
        window_size: The maximum window size.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import MovingAverage
    >>> tracker = MovingAverage()
    >>> for i in range(11):
    ...     tracker.update(i)
    ...
    >>> tracker.smoothed_average()
    5.0

    ```
    """

    def __init__(self, values: Iterable[float] = (), window_size: int = 20) -> None:
        self._deque = deque(values, maxlen=window_size)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(window_size={self.window_size:,})"

    @property
    def count(self) -> float:
        return len(self._deque)

    @property
    def values(self) -> tuple[float, ...]:
        r"""The values in the moving average window."""
        return tuple(self._deque)

    @property
    def window_size(self) -> int:
        r"""The moving average window size."""
        return self._deque.maxlen

    def clone(self) -> Self:
        r"""Return a copy of the current tracker.

        Returns:
            A copy of the current tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage(values=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        >>> tracker_cloned = tracker.clone()
        >>> tracker.update(11)
        >>> tracker.update(12)
        >>> tracker.smoothed_average()
        6.0
        >>> tracker_cloned.smoothed_average()
        5.0

        ```
        """
        return self.__class__(values=tuple(self._deque), window_size=self.window_size)

    def equal(self, other: Any) -> bool:
        r"""Indicate if two trackers are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the trackers are equal, ``False`` otherwise.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker1 = MovingAverage(values=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
        >>> tracker2 = MovingAverage(values=(1.0, 1.0, 1.0))
        >>> tracker1.equal(tracker2)
        False

        ```
        """
        if not isinstance(other, MovingAverage):
            return False
        return self.state_dict() == other.state_dict()

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Load a state to the tracker.

        Args:
            state_dict: A dictionary containing tracker state.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage()
        >>> tracker.load_state_dict(
        ...     {"values": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), "window_size": 20}
        ... )
        >>> tracker.smoothed_average()
        5.0

        ```
        """
        self._deque = deque(state_dict["values"], maxlen=state_dict["window_size"])

    def reset(self) -> None:
        r"""Reset the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.reset()
        >>> tracker.values
        ()

        ```
        """
        self._deque.clear()

    def smoothed_average(self) -> float:
        r"""Compute the smoothed average value.

        Returns:
            The smoothed average value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.smoothed_average()
        5.0

        ```
        """
        if not self._deque:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return torch.as_tensor(self.values).float().mean().item()

    def state_dict(self) -> dict[str, Any]:
        r"""Return a dictionary containing tracker state values.

        Returns:
            The tracker state values in a dict.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.state_dict()
        {'values': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 'window_size': 20}

        ```
        """
        return {"values": self.values, "window_size": self.window_size}

    def update(self, value: float) -> None:
        r"""Update the tracker given a new value.

        Args:
            value: The value to add to the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MovingAverage
        >>> tracker = MovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.smoothed_average()
        5.0

        ```
        """
        self._deque.append(value)


class ExponentialMovingAverage:
    r"""Implement a tracker to track the exponential moving average value
    of float number.

    Args:
        alpha: The smoothing factor such as ``0 < alpha < 1``.
        count: The initial count value.
        smoothed_average: The initial value of the smoothed average.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import ExponentialMovingAverage
    >>> tracker = ExponentialMovingAverage()
    >>> for i in range(11):
    ...     tracker.update(i)
    ...
    >>> tracker.count
    11.0
    >>> tracker.smoothed_average()
    1.036567...

    ```
    """

    def __init__(
        self,
        alpha: float = 0.98,
        count: float = 0,
        smoothed_average: float = 0.0,
    ) -> None:
        self._alpha = float(alpha)
        self._count = float(count)
        self._smoothed_average = float(smoothed_average)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(alpha={self._alpha}, count={self._count:,}, "
            f"smoothed_average={self._smoothed_average}, )"
        )

    @property
    def count(self) -> float:
        r"""The number of examples in the tracker since the last
        reset."""
        return self._count

    def clone(self) -> Self:
        r"""Return a copy of the current tracker.

        Returns:
            A copy of the current tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage(smoothed_average=42.0, count=11)
        >>> tracker_cloned = tracker.clone()
        >>> tracker.update(1)
        >>> tracker.smoothed_average()
        41.18
        >>> tracker.count
        12.0
        >>> tracker_cloned.smoothed_average()
        42.0
        >>> tracker_cloned.count
        11.0

        ```
        """
        return self.__class__(
            alpha=self._alpha,
            count=self._count,
            smoothed_average=self._smoothed_average,
        )

    def equal(self, other: Any) -> bool:
        r"""Indicate if two trackers are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the trackers are equal, ``False`` otherwise.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker1 = ExponentialMovingAverage(count=10, smoothed_average=42.0)
        >>> tracker2 = ExponentialMovingAverage()
        >>> tracker1.equal(tracker2)
        False

        ```
        """
        if not isinstance(other, ExponentialMovingAverage):
            return False
        return self.state_dict() == other.state_dict()

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Load a state to the tracker.

        Args:
            state_dict: A dictionary containing tracker state.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.load_state_dict({"alpha": 0.98, "count": 11, "smoothed_average": 42.0})
        >>> tracker.count
        11.0
        >>> tracker.smoothed_average()
        42.0

        ```
        """
        self._alpha = float(state_dict["alpha"])
        self._count = float(state_dict["count"])
        self._smoothed_average = float(state_dict["smoothed_average"])

    def reset(self) -> None:
        r"""Reset the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.reset()
        >>> tracker.count
        0.0

        ```
        """
        self._count = 0.0
        self._smoothed_average = 0.0

    def smoothed_average(self) -> float:
        r"""Compute the smoothed average value.

        Returns:
            The smoothed average value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.smoothed_average()
        1.036567...

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._smoothed_average

    def state_dict(self) -> dict[str, Any]:
        r"""Return a dictionary containing tracker state values.

        Returns:
            The tracker state values in a dict.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.state_dict()
        {'alpha': 0.98, 'count': 11.0, 'smoothed_average': 1.036567...}

        ```
        """
        return {
            "alpha": self._alpha,
            "count": self._count,
            "smoothed_average": self._smoothed_average,
        }

    def update(self, value: float) -> None:
        r"""Update the tracker given a new value.

        Args:
            value: The value to add to the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ExponentialMovingAverage
        >>> tracker = ExponentialMovingAverage()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.count
        11.0

        ```
        """
        self._smoothed_average = self._alpha * self._smoothed_average + (1.0 - self._alpha) * value
        self._count += 1
