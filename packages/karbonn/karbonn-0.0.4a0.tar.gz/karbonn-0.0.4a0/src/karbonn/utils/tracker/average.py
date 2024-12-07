r"""Implement a tracker to track the average value of float number."""

from __future__ import annotations

__all__ = ["AverageTracker"]

from typing import TYPE_CHECKING, Any

from coola.utils import str_indent, str_mapping

from karbonn.distributed.ddp import SUM, sync_reduce
from karbonn.utils.tracker.base import BaseTracker
from karbonn.utils.tracker.exception import EmptyTrackerError

try:
    from typing import Self  # Introduced in python 3.11
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Iterable


class AverageTracker(BaseTracker):
    r"""Implement a tracker to track the average value of float number.

    Args:
        total: The initial total value.
        count: The initial count value.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import AverageTracker
    >>> tracker = AverageTracker()
    >>> for i in range(11):
    ...     tracker.update(i)
    ...
    >>> tracker.average()
    5.0
    >>> tracker.sum()
    55.0
    >>> tracker.count
    11.0

    ```
    """

    def __init__(self, total: float = 0.0, count: float = 0) -> None:
        self._total = float(total)
        self._count = float(count)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(count={self._count:,}, total={self._total})"

    def __str__(self) -> str:
        stats = str_indent(
            str_mapping(
                {
                    "average": self.average() if self.count else "N/A (empty)",
                    "count": self.count,
                    "total": self.total,
                },
            )
        )
        return f"{self.__class__.__qualname__}(\n  {stats}\n)"

    @property
    def count(self) -> float:
        return self._count

    @property
    def total(self) -> float:
        r"""The total of the values added to the tracker since the last
        reset."""
        return self._total

    def all_reduce(self) -> Self:
        r"""Reduce the tracker values across all machines in such a way
        that all get the final result.

        The total value is reduced by summing all the sum values
        (1 total value per distributed process).
        The count value is reduced by summing all the count values
        (1 count value per distributed process).

        Returns:
            The reduced tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> tracker.update(6)
        >>> reduced_meter = tracker.all_reduce()

        ```
        """
        return self.__class__(
            total=sync_reduce(self._total, SUM),
            count=sync_reduce(self._count, SUM),
        )

    def average(self) -> float:
        r"""Return the average value.

        Returns:
            The average value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.average()
        5.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._total / self._count

    def clone(self) -> Self:
        r"""Return a copy of the current tracker.

        Returns:
            A copy of the current tracker.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker(total=55.0, count=11)
        >>> meter_cloned = tracker.clone()
        >>> tracker.update(1)
        >>> tracker.sum()
        56.0
        >>> tracker.count
        12.0
        >>> meter_cloned.sum()
        55.0
        >>> meter_cloned.count
        11.0

        ```
        """
        return self.__class__(total=self.total, count=self.count)

    def equal(self, other: Any) -> bool:
        r"""Indicate if two trackers are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the trackers are equal, ``False`` otherwise.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tracker import AverageTracker
        >>> meter1 = AverageTracker(total=55.0, count=11)
        >>> meter2 = AverageTracker(total=3.0, count=3)
        >>> meter1.equal(meter2)
        False

        ```
        """
        if not isinstance(other, AverageTracker):
            return False
        return self.state_dict() == other.state_dict()

    def merge(self, trackers: Iterable[Self]) -> Self:
        r"""Merge several trackers with the current tracker and return a
        new tracker.

        Args:
            trackers: The trackers to merge to the current tracker.

        Returns:
            The merged tracker.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tracker import AverageTracker
        >>> meter1 = AverageTracker(total=55.0, count=10)
        >>> meter2 = AverageTracker(total=3.0, count=3)
        >>> meter3 = meter1.merge([meter2])
        >>> meter3.count
        13.0
        >>> meter3.sum()
        58.0

        ```
        """
        count, total = self.count, self.total
        for meter in trackers:
            count += meter.count
            total += meter.total
        return self.__class__(total=total, count=count)

    def merge_(self, trackers: Iterable[Self]) -> None:
        r"""Merge several trackers into the current tracker.

        In-place version of ``merge``.

        Args:
            trackers: The trackers to merge to the current tracker.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tracker import AverageTracker
        >>> meter1 = AverageTracker(total=55.0, count=10)
        >>> meter2 = AverageTracker(total=3.0, count=3)
        >>> meter1.merge_([meter2])
        >>> meter1.count
        13.0
        >>> meter1.sum()
        58.0

        ```
        """
        for meter in trackers:
            self._count += meter.count
            self._total += meter.total

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        r"""Load a tracker to the history tracker.

        Args:
            state_dict: A dictionary containing tracker keys with values.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> tracker.load_state_dict({"count": 11.0, "total": 55.0})
        >>> tracker.count
        11.0
        >>> tracker.sum()
        55.0

        ```
        """
        self._total = float(state_dict["total"])
        self._count = float(state_dict["count"])

    def reset(self) -> None:
        r"""Reset the tracker.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.reset()
        >>> tracker.count
        0.0

        ```
        """
        self._total = 0.0
        self._count = 0.0

    def state_dict(self) -> dict[str, Any]:
        r"""Return a dictionary containing tracker values.

        Returns:
            The tracker values in a dict.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.state_dict()
        {'count': 11.0, 'total': 55.0}

        ```
        """
        return {"count": self._count, "total": self._total}

    def sum(self) -> float:
        r"""Return the sum value.

        Returns:
            The sum value.

        Raises:
            EmptyStateError: if the tracker is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.sum()
        55.0

        ```
        """
        if not self._count:
            msg = "The tracker is empty"
            raise EmptyTrackerError(msg)
        return self._total

    def update(self, value: float, num_examples: float = 1) -> None:
        r"""Update the tracker given a new value and the number of
        examples.

        Args:
            value: The value to add to the tracker.
            num_examples: The number of examples. This argument is
                mainly used to deal with mini-batches of different
                sizes.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import AverageTracker
        >>> tracker = AverageTracker()
        >>> for i in range(11):
        ...     tracker.update(i)
        ...
        >>> tracker.sum()
        55.0

        ```
        """
        num_examples = float(num_examples)
        self._total += float(value) * num_examples
        self._count += num_examples
