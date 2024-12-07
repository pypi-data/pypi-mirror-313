r"""Contain the base class to implement a tracker."""

from __future__ import annotations

__all__ = ["BaseTracker"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

try:
    from typing import Self  # Introduced in python 3.11
except ImportError:  # pragma: no cover
    from typing_extensions import Self


class BaseTracker(ABC):
    r"""Define the base class to implement a tracker.

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

    @property
    @abstractmethod
    def count(self) -> float | int:
        r"""The number of examples in the tracker since the last
        reset."""

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        r"""Update the tracker given new data.

        The exact signature for this method depends on each metric
        state implementation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

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
