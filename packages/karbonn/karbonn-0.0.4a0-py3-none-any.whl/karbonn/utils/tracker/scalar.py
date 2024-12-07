r"""Implement a tracker to track some statistics about a scalar
value."""

from __future__ import annotations

__all__ = ["ScalarTracker"]

from collections import deque
from typing import TYPE_CHECKING, Any

import torch
from coola.utils import str_indent, str_mapping

from karbonn.utils.tracker import BaseTracker
from karbonn.utils.tracker.exception import EmptyTrackerError

try:
    from typing import Self  # Introduced in python 3.11
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


class ScalarTracker(BaseTracker):
    r"""Implement a tracker to track some statistics about a scalar
    value.

    This tracker tracks the following values:

        - the sum of the values
        - the number of values
        - the minimum value
        - the maximum value
        - the last N values which are used to compute the median value.

    Args:
        total: The initial total value.
        count: The initial count value.
        min_value: The initial minimum value.
        max_value: The initial maximum value.
        values: The initial last values to store. These values are
            used to estimate the standard deviation and median.
        max_size: The maximum size used to store the last values
            because it may not be possible to store all the values.
            This parameter is used to compute the median only on the
            N last values.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import ScalarTracker
    >>> tracker = ScalarTracker()
    >>> tracker.update(6)
    >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
    >>> print(tracker)
    ScalarTracker(
      (average): 3.0
      (count): 7.0
      (max): 6.0
      (median): 3.0
      (min): 0.0
      (std): 2.16024...
      (sum): 21.0
    )
    >>> tracker.average()
    3.0

    ```
    """

    def __init__(
        self,
        total: float = 0.0,
        count: float = 0,
        min_value: float = float("inf"),
        max_value: float = -float("inf"),
        values: Iterable[float] = (),
        max_size: int = 100,
    ) -> None:
        self._total = float(total)
        self._count = float(count)
        self._min_value = float(min_value)
        self._max_value = float(max_value)
        # Store only the N last values to scale to large number of values.
        self._values = deque(values, maxlen=max_size)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(count={self._count:,}, total={self._total}, "
            f"min_value={self._min_value}, max_value={self._max_value}, "
            f"max_size={self._values.maxlen:,})"
        )

    def __str__(self) -> str:
        count = self.count
        stats = str_indent(
            str_mapping(
                {
                    "average": self.average() if count else "N/A (empty)",
                    "count": count,
                    "max": self.max() if count else "N/A (empty)",
                    "median": self.median() if count else "N/A (empty)",
                    "min": self.min() if count else "N/A (empty)",
                    "std": self.std() if count else "N/A (empty)",
                    "sum": self.sum() if count else "N/A (empty)",
                },
            )
        )
        return f"{self.__class__.__qualname__}(\n  {stats}\n)"

    @property
    def count(self) -> float:
        r"""The number of examples in the tracker."""
        return self._count

    @property
    def total(self) -> float:
        r"""The total of the values added to the tracker."""
        return self._total

    @property
    def values(self) -> tuple[float, ...]:
        r"""The values store in this tracker.

        If there are more values that the maximum size, only the last
        values are returned.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.values
        (1.0, 2.0, 3.0, 4.0, 5.0, 0.0)

        ```
        """
        return tuple(self._values)

    def average(self) -> float:
        r"""Return the average value.

        Returns:
            The average value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.average()
        2.5

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._total / float(self._count)

    def clone(self) -> Self:
        r"""Return a copy of the current tracker.

        Returns:
            A copy of the current tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker_cloned = tracker.clone()
        >>> tracker.update(11)
        >>> tracker.total
        26.0
        >>> tracker_cloned.total
        15.0

        ```
        """
        return self.__class__(
            total=self._total,
            count=self._count,
            min_value=self._min_value,
            max_value=self._max_value,
            values=self._values,
            max_size=self._values.maxlen,
        )

    def equal(self, other: Any) -> bool:
        r"""Indicate if two trackers are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the trackers are equal, ``False`` otherwise.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker1 = ScalarTracker()
        >>> tracker1.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker2 = ScalarTracker()
        >>> tracker2.update_sequence([1, 1, 1])
        >>> tracker1.equal(tracker2)
        False

        ```
        """
        if not isinstance(other, ScalarTracker):
            return False
        return self.state_dict() == other.state_dict()

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Load a state to the history tracker.

        Args:
            state_dict: Dictionary containing tracker state.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.load_state_dict(
        ...     {
        ...         "count": 6,
        ...         "total": 15.0,
        ...         "values": (1.0, 2.0, 3.0, 4.0, 5.0, 0.0),
        ...         "max_value": 5.0,
        ...         "min_value": 0.0,
        ...     }
        ... )
        >>> tracker.count
        6.0
        >>> tracker.min()
        0.0
        >>> tracker.max()
        5.0
        >>> tracker.sum()
        15.0

        ```
        """
        self._total = float(state_dict["total"])
        self._count = float(state_dict["count"])
        self._max_value = float(state_dict["max_value"])
        self._min_value = float(state_dict["min_value"])
        self._values.clear()
        self._values.extend(state_dict["values"])

    def max(self) -> float:
        r"""Get the max value.

        Returns:
            The max value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.max()
        5.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._max_value

    def median(self) -> float:
        r"""Compute the median value from the last examples.

        If there are more values than the maximum window size, only
        the last examples are used. Internally, this tracker uses a
        deque to track the last values and the median value is
        computed on the values in the deque. The median is not unique
        for input tensors with an even number of elements. In this
        case the lower of the two medians is returned.

        Returns:
            The median value from the last examples.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5])
        >>> tracker.average()
        3.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return torch.as_tensor(list(self._values)).median().item()

    def merge(self, trackers: Iterable[Self]) -> Self:
        r"""Merge several trackers with the current tracker and returns a
        new tracker.

        Only the values of the current tracker are copied to the merged
        tracker.

        Args:
            trackers: The trackers to merge to the current tracker.

        Returns:
            The merged tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker1 = ScalarTracker()
        >>> tracker1.update_sequence((4, 5, 6, 7, 8, 3))
        >>> tracker2 = ScalarTracker()
        >>> tracker2.update_sequence([1, 1, 1])
        >>> tracker3 = tracker1.merge([tracker2])
        >>> tracker3.count
        9.0
        >>> tracker3.max()
        8.0
        >>> tracker3.min()
        1.0
        >>> tracker3.sum()
        36.0

        ```
        """
        count, total = self._count, self._total
        min_value, max_value = self._min_value, self._max_value
        for tracker in trackers:
            count += tracker.count
            total += tracker.total
            min_value = min(min_value, tracker._min_value)
            max_value = max(max_value, tracker._max_value)
        return ScalarTracker(
            total=total,
            count=count,
            min_value=min_value,
            max_value=max_value,
            values=self.values,
            max_size=self._values.maxlen,
        )

    def merge_(self, trackers: Iterable[ScalarTracker]) -> None:
        r"""Merge several trackers into the current tracker.

        In-place version of ``merge``.

        Only the values of the current tracker are copied to the merged
        tracker.

        Args:
            trackers: The trackers to merge to the current tracker.

        Returns:
            The merged tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker1 = ScalarTracker()
        >>> tracker1.update_sequence((4, 5, 6, 7, 8, 3))
        >>> tracker2 = ScalarTracker()
        >>> tracker2.update_sequence([1, 1, 1])
        >>> tracker1.merge_([tracker2])
        >>> tracker1.count
        9.0
        >>> tracker1.max()
        8.0
        >>> tracker1.min()
        1.0
        >>> tracker1.sum()
        36.0

        ```
        """
        for tracker in trackers:
            self._count += tracker.count
            self._total += tracker.total
            self._min_value = min(self._min_value, tracker._min_value)
            self._max_value = max(self._max_value, tracker._max_value)

    def min(self) -> float:
        r"""Get the min value.

        Returns:
            The min value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.min()
        0.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._min_value

    def reset(self) -> None:
        r"""Reset the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.reset()
        >>> tracker.count
        0.0
        >>> tracker.total
        0.0

        ```
        """
        self._total = 0.0
        self._count = 0.0
        self._min_value = float("inf")
        self._max_value = -float("inf")
        self._values.clear()

    def state_dict(self) -> dict[str, Any]:
        r"""Return a dictionary containing state values.

        Returns:
            The state values in a dict.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.state_dict()
        {'count': 6.0, 'total': 15.0, 'values': (1.0, 2.0, 3.0, 4.0, 5.0, 0.0), 'max_value': 5.0, 'min_value': 0.0}

        ```
        """
        return {
            "count": self._count,
            "total": self._total,
            "values": tuple(self._values),
            "max_value": self._max_value,
            "min_value": self._min_value,
        }

    def std(self) -> float:
        r"""Return the standard deviation based on the last examples
        added to the tracker.

        If there are more values than the maximum window size, only
        the last examples are used. Internally, this tracker uses a
        deque to track the last values and the standard deviation
        is computed on the values in the deque.

        Returns:
            The standard deviation from the last examples.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.std()  # xdoctest: +ELLIPSIS
        1.8708287477...

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return torch.as_tensor(self.values, dtype=torch.float).std(dim=0).item()

    def sum(self) -> float:
        r"""Return the sum value.

        Returns:
            The sum value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.sum()
        15.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._total

    def update(self, value: float) -> None:
        r"""Update the tracker given a new value.

        Args:
            value: The value to add to the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update(6)
        >>> tracker.count
        1.0
        >>> tracker.sum()
        6.0

        ```
        """
        value = float(value)
        self._total += value
        self._count += 1
        self._min_value = min(self._min_value, value)
        self._max_value = max(self._max_value, value)
        self._values.append(value)

    def update_sequence(self, values: Sequence[float]) -> None:
        r"""Update the tracker given a list/tuple of values.

        Args:
            values: The list/tuple of values to add to the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import ScalarTracker
        >>> tracker = ScalarTracker()
        >>> tracker.update_sequence([1, 2, 3, 4, 5, 0])
        >>> tracker.count
        6.0

        ```
        """
        self._total += float(sum(values))
        self._count += len(values)
        self._min_value = float(min(self._min_value, *values))
        self._max_value = float(max(self._max_value, *values))
        self._values.extend(float(v) for v in values)
