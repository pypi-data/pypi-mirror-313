r"""Contain the error-based metric states."""

from __future__ import annotations

__all__ = [
    "ErrorState",
    "ExtendedErrorState",
    "MeanErrorState",
    "NormalizedMeanSquaredErrorState",
    "RootMeanErrorState",
]

import math
from typing import TYPE_CHECKING, Any

from coola import objects_are_equal
from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from minrecord import BaseRecord, MinScalarRecord

from karbonn.metric.base import EmptyMetricError
from karbonn.metric.state.base import BaseState
from karbonn.utils.tensor import to_tensor
from karbonn.utils.tracker import (
    MeanTensorTracker,
    ScalableTensorTracker,
    TensorTracker,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    import torch


class ErrorState(BaseState):
    r"""Implement a metric state to capture some metrics about the
    errors.

    This state has a constant space complexity.

    Args:
        tracker: The value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import ErrorState
    >>> state = ErrorState()
    >>> state
    ErrorState(
      (tracker): ScalableTensorTracker(count=0, total=0.0, min_value=inf, max_value=-inf)
      (track_count): True
    )
    >>> state.get_records("error_")
    (MinScalarRecord(name=error_mean, max_size=10, size=0),
     MinScalarRecord(name=error_min, max_size=10, size=0),
     MinScalarRecord(name=error_max, max_size=10, size=0),
     MinScalarRecord(name=error_sum, max_size=10, size=0))
    >>> state.update(torch.arange(6))
    >>> state.value("error_")
    {'error_mean': 2.5,
     'error_min': 0.0,
     'error_max': 5.0,
     'error_sum': 15.0,
     'error_count': 6}

    ```
    """

    def __init__(
        self, tracker: ScalableTensorTracker | None = None, track_count: bool = True
    ) -> None:
        self._tracker = tracker or ScalableTensorTracker()
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

    def clone(self) -> ErrorState:
        return self.__class__(tracker=self._tracker.clone(), track_count=self._track_count)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, ErrorState):
            return False
        return self._track_count == other._track_count and self._tracker.equal(other._tracker)

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (
            MinScalarRecord(name=f"{prefix}mean{suffix}"),
            MinScalarRecord(name=f"{prefix}min{suffix}"),
            MinScalarRecord(name=f"{prefix}max{suffix}"),
            MinScalarRecord(name=f"{prefix}sum{suffix}"),
        )

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, error: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            error: A tensor of errors.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ErrorState
        >>> state = ErrorState()
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 2.5,
         'error_min': 0.0,
         'error_max': 5.0,
         'error_sum': 15.0,
         'error_count': 6}

        ```
        """
        self._tracker.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {
            f"{prefix}mean{suffix}": tracker.mean(),
            f"{prefix}min{suffix}": tracker.min(),
            f"{prefix}max{suffix}": tracker.max(),
            f"{prefix}sum{suffix}": tracker.sum(),
        }
        if self._track_count:
            results[f"{prefix}count{suffix}"] = tracker.count
        return results


class ExtendedErrorState(BaseState):
    r"""Implement a metric state to capture some metrics about the
    errors.

    This state stores all the error values, so it does not scale to large
    datasets. This state has a linear space complexity.

    Args:
        quantiles: The quantile values to evaluate.
        tracker: The value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import ExtendedErrorState
    >>> state = ExtendedErrorState(quantiles=[0.5, 0.9])
    >>> state
    ExtendedErrorState(
      (quantiles): tensor([0.5000, 0.9000])
      (tracker): TensorTracker(count=0)
      (track_count): True
    )
    >>> state.get_records("error_")
    (MinScalarRecord(name=error_mean, max_size=10, size=0),
     MinScalarRecord(name=error_median, max_size=10, size=0),
     MinScalarRecord(name=error_min, max_size=10, size=0),
     MinScalarRecord(name=error_max, max_size=10, size=0),
     MinScalarRecord(name=error_sum, max_size=10, size=0),
     MinScalarRecord(name=error_quantile_0.5, max_size=10, size=0),
     MinScalarRecord(name=error_quantile_0.9, max_size=10, size=0))
    >>> state.update(torch.arange(11))
    >>> state.value("error_")
    {'error_mean': 5.0,
     'error_median': 5,
     'error_min': 0,
     'error_max': 10,
     'error_sum': 55,
     'error_std': 3.316...,
     'error_quantile_0.5': 5.0,
     'error_quantile_0.9': 9.0,
     'error_count': 11}

    ```
    """

    def __init__(
        self,
        quantiles: torch.Tensor | Sequence[float] = (),
        tracker: TensorTracker | None = None,
        track_count: bool = True,
    ) -> None:
        self._quantiles = to_tensor(quantiles)
        self._tracker = tracker or TensorTracker()
        self._track_count = bool(track_count)

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "quantiles": self._quantiles,
                    "tracker": self._tracker,
                    "track_count": self._track_count,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "quantiles": self._quantiles,
                    "tracker": self._tracker,
                    "count": self.count,
                    "track_count": self._track_count,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def count(self) -> int:
        return self._tracker.count

    def clone(self) -> ExtendedErrorState:
        return self.__class__(
            quantiles=self._quantiles,
            tracker=self._tracker.clone(),
            track_count=self._track_count,
        )

    def equal(self, other: Any) -> bool:
        if not isinstance(other, ExtendedErrorState):
            return False
        return (
            self._track_count == other._track_count
            and self._tracker.equal(other._tracker)
            and objects_are_equal(self._quantiles, other._quantiles)
        )

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        trackers = [
            MinScalarRecord(name=f"{prefix}mean{suffix}"),
            MinScalarRecord(name=f"{prefix}median{suffix}"),
            MinScalarRecord(name=f"{prefix}min{suffix}"),
            MinScalarRecord(name=f"{prefix}max{suffix}"),
            MinScalarRecord(name=f"{prefix}sum{suffix}"),
        ]
        trackers.extend(
            MinScalarRecord(name=f"{prefix}quantile_{q:g}{suffix}") for q in self._quantiles
        )
        return tuple(trackers)

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, error: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            error: A tensor of errors.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ExtendedErrorState
        >>> state = ExtendedErrorState(quantiles=[0.5, 0.9])
        >>> state.update(torch.arange(11))
        >>> state.value("error_")
        {'error_mean': 5.0,
         'error_median': 5,
         'error_min': 0,
         'error_max': 10,
         'error_sum': 55,
         'error_std': 3.316...,
         'error_quantile_0.5': 5.0,
         'error_quantile_0.9': 9.0,
         'error_count': 11}

        ```
        """
        self._tracker.update(error.detach().cpu())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {
            f"{prefix}mean{suffix}": tracker.mean(),
            f"{prefix}median{suffix}": tracker.median(),
            f"{prefix}min{suffix}": tracker.min(),
            f"{prefix}max{suffix}": tracker.max(),
            f"{prefix}sum{suffix}": tracker.sum(),
            f"{prefix}std{suffix}": tracker.std(),
        }
        if self._quantiles.numel() > 0:
            values = tracker.quantile(self._quantiles)
            for q, v in zip(self._quantiles, values):
                results[f"{prefix}quantile_{q:g}{suffix}"] = v.item()
        if self._track_count:
            results[f"{prefix}count{suffix}"] = tracker.count
        return results


class MeanErrorState(BaseState):
    r"""Implement a metric state to capture the mean error value.

    This state has a constant space complexity.

    Args:
        tracker: The mean value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import MeanErrorState
    >>> state = MeanErrorState()
    >>> state
    MeanErrorState(
      (tracker): MeanTensorTracker(count=0, total=0.0)
      (track_count): True
    )
    >>> state.get_records("error_")
    (MinScalarRecord(name=error_mean, max_size=10, size=0),)
    >>> state.update(torch.arange(6))
    >>> state.value("error_")
    {'error_mean': 2.5, 'error_count': 6}

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

    def clone(self) -> MeanErrorState:
        return self.__class__(tracker=self._tracker.clone(), track_count=self._track_count)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, MeanErrorState):
            return False
        return self._track_count == other._track_count and self._tracker.equal(other._tracker)

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (MinScalarRecord(name=f"{prefix}mean{suffix}"),)

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, error: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            error: A tensor of errors.


        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import MeanErrorState
        >>> state = MeanErrorState()
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 2.5, 'error_count': 6}

        ```
        """
        self._tracker.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {f"{prefix}mean{suffix}": tracker.mean()}
        if self._track_count:
            results[f"{prefix}count{suffix}"] = tracker.count
        return results


class RootMeanErrorState(BaseState):
    r"""Implement a metric state to capture the root mean error value.

    This state has a constant space complexity.

    Args:
        tracker: The mean value tracker.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import RootMeanErrorState
    >>> state = RootMeanErrorState()
    >>> state
    RootMeanErrorState(
      (tracker): MeanTensorTracker(count=0, total=0.0)
      (track_count): True
    )
    >>> state.get_records("error_")
    (MinScalarRecord(name=error_mean, max_size=10, size=0),)
    >>> state.update(torch.arange(6))
    >>> state.value("error_")
    {'error_mean': 1.581..., 'error_count': 6}

    ```
    """

    def __init__(self, tracker: MeanTensorTracker | None = None, track_count: bool = True) -> None:
        self._tracker = tracker or MeanTensorTracker()
        self._track_count = bool(track_count)

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"tracker": self._tracker, "track_count": self._track_count}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def count(self) -> int:
        return self._tracker.count

    def clone(self) -> RootMeanErrorState:
        return self.__class__(tracker=self._tracker.clone(), track_count=self._track_count)

    def equal(self, other: Any) -> bool:
        if not isinstance(other, RootMeanErrorState):
            return False
        return self._track_count == other._track_count and self._tracker.equal(other._tracker)

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (MinScalarRecord(name=f"{prefix}mean{suffix}"),)

    def reset(self) -> None:
        self._tracker.reset()

    def update(self, error: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            error: A tensor of errors.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import RootMeanErrorState
        >>> state = RootMeanErrorState()
        >>> state.update(torch.arange(6))
        >>> state.value("error_")
        {'error_mean': 1.581..., 'error_count': 6}

        ```
        """
        self._tracker.update(error.detach())

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        tracker = self._tracker.all_reduce()
        if not tracker.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {f"{prefix}mean{suffix}": math.sqrt(tracker.mean())}
        if self._track_count:
            results[f"{prefix}count{suffix}"] = tracker.count
        return results


class NormalizedMeanSquaredErrorState(BaseState):
    r"""Implement a metric state to capture the normalized mean squared
    error value.

    This state has a constant space complexity.

    Args:
        squared_errors: The value tracker for squared errors.
        squared_targets: The value tracker for squared targets.
        track_count: If ``True``, the state tracks and
            returns the number of predictions.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric.state import NormalizedMeanSquaredErrorState
    >>> state = NormalizedMeanSquaredErrorState()
    >>> state
    NormalizedMeanSquaredErrorState(
      (squared_errors): MeanTensorTracker(count=0, total=0.0)
      (squared_targets): MeanTensorTracker(count=0, total=0.0)
      (track_count): True
    )
    >>> state.get_records("nmse_")
    (MinScalarRecord(name=nmse_mean, max_size=10, size=0),)
    >>> state.update(torch.arange(6), torch.ones(6))
    >>> state.value("nmse_")
    {'nmse_mean': 9.166..., 'nmse_count': 6}

    ```
    """

    def __init__(
        self,
        squared_errors: MeanTensorTracker | None = None,
        squared_targets: MeanTensorTracker | None = None,
        track_count: bool = True,
    ) -> None:
        self._squared_errors = squared_errors or MeanTensorTracker()
        self._squared_targets = squared_targets or MeanTensorTracker()
        self._track_count = bool(track_count)

    def __repr__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "squared_errors": self._squared_errors,
                    "squared_targets": self._squared_targets,
                    "track_count": self._track_count,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def count(self) -> int:
        return self._squared_errors.count

    def clone(self) -> NormalizedMeanSquaredErrorState:
        return self.__class__(
            squared_errors=self._squared_errors.clone(),
            squared_targets=self._squared_targets.clone(),
            track_count=self._track_count,
        )

    def equal(self, other: Any) -> bool:
        if not isinstance(other, NormalizedMeanSquaredErrorState):
            return False
        return (
            self._track_count == other._track_count
            and self._squared_errors.equal(other._squared_errors)
            and self._squared_targets.equal(other._squared_targets)
        )

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return (MinScalarRecord(name=f"{prefix}mean{suffix}"),)

    def reset(self) -> None:
        self._squared_errors.reset()
        self._squared_targets.reset()

    def update(self, error: torch.Tensor, target: torch.Tensor) -> None:
        r"""Update the metric state with a new tensor of errors.

        Args:
            error: A tensor of errors.
            target: A tensor with the target values.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import NormalizedMeanSquaredErrorState
        >>> state = NormalizedMeanSquaredErrorState()
        >>> state.update(torch.arange(6), torch.ones(6))
        >>> state.value("nmse_")
        {'nmse_mean': 9.166..., 'nmse_count': 6}

        ```
        """
        self._squared_errors.update(error.detach().pow(2))
        self._squared_targets.update(target.detach().pow(2))

    def value(self, prefix: str = "", suffix: str = "") -> dict[str, int | float]:
        squared_errors = self._squared_errors.all_reduce()
        squared_targets = self._squared_targets.all_reduce()
        if not squared_errors.count:
            msg = f"{self.__class__.__qualname__} is empty"
            raise EmptyMetricError(msg)

        results = {f"{prefix}mean{suffix}": squared_errors.sum() / squared_targets.sum()}
        if self._track_count:
            results[f"{prefix}count{suffix}"] = squared_errors.count
        return results
