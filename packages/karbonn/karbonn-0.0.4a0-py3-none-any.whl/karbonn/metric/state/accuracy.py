r"""Contain the accuracy-based metric states."""

from __future__ import annotations

__all__ = ["AccuracyState"]

from typing import TYPE_CHECKING, Any

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from minrecord import BaseRecord, MaxScalarRecord, MinScalarRecord

from karbonn.metric.base import EmptyMetricError
from karbonn.metric.state.base import BaseState
from karbonn.utils.tracker import MeanTensorTracker

if TYPE_CHECKING:
    import torch


class AccuracyState(BaseState):
    r"""Implement a metric state to compute the accuracy.

    This state has a constant space complexity.

    Args:
        tracker: The mean value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import AccuracyState
    >>> state = AccuracyState()
    >>> state
    AccuracyState(
      (tracker): MeanTensorTracker(count=0, total=0.0)
      (track_count): True
    )
    >>> state.get_records()
    (MaxScalarRecord(name=accuracy, max_size=10, size=0),)
    >>> state.update(torch.eye(4))
    >>> state.value()
    {'accuracy': 0.25, 'count': 16}

    ```
    """

    def __init__(self, tracker: MeanTensorTracker | None = None, track_count: bool = True) -> None:
        self._tracker = tracker or MeanTensorTracker()
        self._track_count = bool(track_count)

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping({"tracker": self._tracker, "track_count": self._track_count})
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "tracker": self._tracker,
                    "count": f"{self.count:,}",
                    "track_count": self._track_count,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def count(self) -> int:
        return self._tracker.count

    def clone(self) -> AccuracyState:
        return self.__class__(tracker=self._tracker.clone(), track_count=self._track_count)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, AccuracyState):
            return False
        return self._track_count == other._track_count and self._tracker.equal(other._tracker)

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (MaxScalarRecord(name=f"{prefix}accuracy{suffix}"),)

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, correct: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            correct: A tensor that indicates the correct predictions.
                ``1`` indicates a correct prediction and ``0``
                indicates a bad prediction.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import AccuracyState
        >>> state = AccuracyState()
        >>> state.update(torch.eye(4))
        >>> state.value()
        {'accuracy': 0.25, 'count': 16}

        ```
        """
        self._tracker.update(correct.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {f"{prefix}accuracy{suffix}": tracker.mean()}
        if self._track_count:
            results[f"{prefix}count{suffix}"] = tracker.count
        return results


class ExtendedAccuracyState(BaseState):
    r"""Implement a metric state to compute the accuracy and other
    metrics.

    This state has a constant space complexity.

    Args:
        tracker: The mean value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import ExtendedAccuracyState
    >>> state = ExtendedAccuracyState()
    >>> state
    ExtendedAccuracyState(
      (tracker): MeanTensorTracker(count=0, total=0.0)
      (track_count): True
    )
    >>> state.get_records()
    (MaxScalarRecord(name=accuracy, max_size=10, size=0),
     MinScalarRecord(name=error, max_size=10, size=0),
     MaxScalarRecord(name=count_correct, max_size=10, size=0),
     MinScalarRecord(name=count_incorrect, max_size=10, size=0))
    >>> state.update(torch.eye(4))
    >>> state.value()
    {'accuracy': 0.25,
     'error': 0.75,
     'count_correct': 4,
     'count_incorrect': 12,
     'count': 16}

    ```
    """

    def __init__(self, tracker: MeanTensorTracker | None = None, track_count: bool = True) -> None:
        self._tracker = tracker or MeanTensorTracker()
        self._track_count = bool(track_count)

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping({"tracker": self._tracker, "track_count": self._track_count})
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "tracker": self._tracker,
                    "count": f"{self.count:,}",
                    "track_count": self._track_count,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def count(self) -> int:
        return self._tracker.count

    def clone(self) -> ExtendedAccuracyState:
        return self.__class__(tracker=self._tracker.clone(), track_count=self._track_count)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, ExtendedAccuracyState):
            return False
        return self._track_count == other._track_count and self._tracker.equal(other._tracker)

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (
            MaxScalarRecord(name=f"{prefix}accuracy{suffix}"),
            MinScalarRecord(name=f"{prefix}error{suffix}"),
            MaxScalarRecord(name=f"{prefix}count_correct{suffix}"),
            MinScalarRecord(name=f"{prefix}count_incorrect{suffix}"),
        )

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, correct: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            correct: A tensor that indicates the correct predictions.
                ``1`` indicates a correct prediction and ``0``
                indicates a bad prediction.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ExtendedAccuracyState
        >>> state = ExtendedAccuracyState()
        >>> state.update(torch.eye(4))
        >>> state.value()
        {'accuracy': 0.25,
         'error': 0.75,
         'count_correct': 4,
         'count_incorrect': 12,
         'count': 16}

        ```
        """
        self._tracker.update(correct.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        accuracy = tracker.mean()
        count_correct = int(tracker.sum())
        count = tracker.count
        results = {
            f"{prefix}accuracy{suffix}": accuracy,
            f"{prefix}error{suffix}": 1.0 - accuracy,
        }
        if self._track_count:
            results.update(
                {
                    f"{prefix}count_correct{suffix}": count_correct,
                    f"{prefix}count_incorrect{suffix}": count - count_correct,
                    f"{prefix}count{suffix}": count,
                }
            )
        return results
