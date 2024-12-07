r"""Contain the base class to implement a metric state."""

from __future__ import annotations

__all__ = ["BaseState", "is_state_config", "setup_state"]

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from coola.equality.comparators import BaseEqualityComparator
from coola.equality.handlers import EqualHandler, SameObjectHandler, SameTypeHandler
from coola.equality.testers import EqualityTester

from karbonn.utils.imports import check_objectory, is_objectory_available

if TYPE_CHECKING:
    from coola.equality import EqualityConfig
    from minrecord import BaseRecord


if is_objectory_available():
    import objectory
    from objectory import AbstractFactory
else:  # pragma: no cover
    objectory = Mock()

    AbstractFactory = ABCMeta


logger = logging.getLogger(__name__)


class BaseState(ABC, metaclass=AbstractFactory):
    r"""Define a base class to implement a metric state.

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

    @property
    @abstractmethod
    def count(self) -> int:
        r"""The number of predictions in the state."""

    def clone(self) -> BaseState:
        r"""Create a copy of the current state.

        Returns:
            A copy of the current state.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ErrorState
        >>> state = ErrorState()
        >>> state.update(torch.arange(6))
        >>> state_cloned = state.clone()
        >>> state.update(torch.ones(3))
        >>> state
        ErrorState(
          (tracker): ScalableTensorTracker(count=9, total=18.0, min_value=0, max_value=5)
          (track_count): True
        )
        >>> state_cloned
        ErrorState(
          (tracker): ScalableTensorTracker(count=6, total=15.0, min_value=0.0, max_value=5.0)
          (track_count): True
        )

        ```
        """

    @abstractmethod
    def equal(self, other: Any) -> bool:
        r"""Indicate if two metric states are equal or not.

        Args:
                other: The other metric state to compare.

        Returns:
                ``True`` if the two metric states are equal,
                    otherwise ``False``.

            Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ErrorState
        >>> from karbonn.utils.tracker import ScalableTensorTracker
        >>> state = ErrorState()
        >>> state.equal(ErrorState())
        True
        >>> state.equal(
        ...     ErrorState(ScalableTensorTracker(count=4, total=10.0, min_value=0.0, max_value=5.0))
        ... )
        False

        ```
        """

    @abstractmethod
    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        r"""Get the records for the metrics associated to the current
        state.

        Args:
            prefix: The key prefix in the record names.
            suffix: The key suffix in the record names.

        Returns:
            tuple: The records.

        Example usage:

        ```pycon

        >>> from karbonn.metric.state import ErrorState
        >>> state = ErrorState()
        >>> state.get_records("error_")
        (MinScalarRecord(name=error_mean, max_size=10, size=0),
         MinScalarRecord(name=error_min, max_size=10, size=0),
         MinScalarRecord(name=error_max, max_size=10, size=0),
         MinScalarRecord(name=error_sum, max_size=10, size=0))

        ```
        """

    @abstractmethod
    def reset(self) -> None:
        r"""Reset the state.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ErrorState
        >>> state = ErrorState()
        >>> state.update(torch.arange(6))
        >>> state
        ErrorState(
          (tracker): ScalableTensorTracker(count=6, total=15.0, min_value=0, max_value=5)
          (track_count): True
        )
        >>> state.reset()
        >>> state
        ErrorState(
          (tracker): ScalableTensorTracker(count=0, total=0.0, min_value=inf, max_value=-inf)
          (track_count): True
        )

        ```
        """

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        r"""Update the metric state.

        The exact signature for this method depends on each metric
        state implementation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric.state import ErrorState
        >>> state = ErrorState()
        >>> state.update(torch.arange(6))
        >>> state
        ErrorState(
          (tracker): ScalableTensorTracker(count=6, total=15.0, min_value=0, max_value=5)
          (track_count): True
        )

        ```
        """

    @abstractmethod
    def value(self, prefix: str = "", suffix: str = "") -> dict[str, float]:
        r"""Compute the metrics given the current state.

        Args:
            prefix: The key prefix in the returned dictionary.
            suffix: The key suffix in thenreturned dictionary.

        Returns:
            The metric values.

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


def is_state_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseState``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseState`` object, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.metric.state import is_state_config
    >>> is_state_config({"_target_": "karbonn.metric.state.ErrorState"})
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, BaseState)


def setup_state(state: BaseState | dict) -> BaseState:
    r"""Set up a ``BaseState`` object.

    Args:
        state: The state or its configuration.

    Returns:
        The instantiated ``BaseState`` object.

    Example usage:

    ```pycon

    >>> from karbonn.metric.state import setup_state
    >>> state = setup_state({"_target_": "karbonn.metric.state.ErrorState"})
    >>> state
    ErrorState(
      (tracker): ScalableTensorTracker(count=0, total=0.0, min_value=inf, max_value=-inf)
      (track_count): True
    )

    ```
    """
    if isinstance(state, dict):
        logger.info("Initializing a 'BaseState' object from its configuration...")
        check_objectory()
        state = BaseState.factory(**state)
    if not isinstance(state, BaseState):
        logger.warning(f"state is not a 'BaseState' (received: {type(state)})")
    return state


class StateEqualityComparator(BaseEqualityComparator[BaseState]):
    r"""Implement an equality comparator for ``BaseState`` objects."""

    def __init__(self) -> None:
        self._handler = SameObjectHandler()
        self._handler.chain(SameTypeHandler()).chain(EqualHandler())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> StateEqualityComparator:
        return self.__class__()

    def equal(self, actual: BaseState, expected: Any, config: EqualityConfig) -> bool:
        return self._handler.handle(actual, expected, config=config)


if not EqualityTester.has_comparator(BaseState):  # pragma: no cover
    EqualityTester.add_comparator(BaseState, StateEqualityComparator())
