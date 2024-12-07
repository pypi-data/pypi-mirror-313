r"""Contain a base class to implement a metric with a state."""

from __future__ import annotations

__all__ = ["BaseStateMetric"]

from typing import TYPE_CHECKING

from coola.utils import repr_mapping

from karbonn.metric import BaseMetric
from karbonn.metric.state import BaseState, setup_state

if TYPE_CHECKING:
    from minrecord import BaseRecord


class BaseStateMetric(BaseMetric):
    r"""Define a base class to implement a metric with a state.

    Child classes must implement the following method:

        - ``forward``

    Args:
        state: The metric state or its configuration.
    """

    def __init__(self, state: BaseState | dict) -> None:
        super().__init__()
        self._state = setup_state(state)

    @property
    def state(self) -> BaseState:
        return self._state

    def extra_repr(self) -> str:
        return repr_mapping({"state": self._state})

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        return self._state.get_records(prefix, suffix)

    def reset(self) -> None:
        self._state.reset()

    def value(self, prefix: str = "", suffix: str = "") -> dict:
        return self._state.value(prefix=prefix, suffix=suffix)
