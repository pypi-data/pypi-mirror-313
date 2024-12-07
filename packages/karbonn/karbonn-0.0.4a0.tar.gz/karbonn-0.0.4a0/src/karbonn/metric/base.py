r"""Contain the base class to implement a metric."""

from __future__ import annotations

__all__ = ["BaseMetric", "EmptyMetricError", "setup_metric"]

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from torch.nn import Module

from karbonn.utils.imports import check_objectory, is_objectory_available

if TYPE_CHECKING:
    from minrecord import BaseRecord

if is_objectory_available():
    from objectory import AbstractFactory
else:  # pragma: no cover
    AbstractFactory = ABCMeta


logger = logging.getLogger(__name__)


class BaseMetric(Module, metaclass=AbstractFactory):
    r"""Define the base class to implement a metric.

    This class is used to register the metric using the metaclass
    factory. Child classes must implement the following methods:

        - ``forward``
        - ``get_records``
        - ``reset``
        - ``value``
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

        >>> from karbonn.metric import AbsoluteError
        >>> metric = AbsoluteError()
        >>> metric.get_records("error_")
        (MinScalarRecord(name=error_mean, max_size=10, size=0),
         MinScalarRecord(name=error_min, max_size=10, size=0),
         MinScalarRecord(name=error_max, max_size=10, size=0),
         MinScalarRecord(name=error_sum, max_size=10, size=0))

        ```
        """

    @abstractmethod
    def reset(self) -> None:
        r"""Reset the metric."""

    @abstractmethod
    def value(self, prefix: str = "", suffix: str = "") -> dict:
        r"""Evaluate the metric and return the results given all the
        examples previously seen.

        Args:
            prefix: The key prefix in the returned dictionary.
            suffix: The key suffix in the returned dictionary.

        Returns:
             The results of the metric.
        """


class EmptyMetricError(Exception):
    r"""Raised when an empty metric is evaluated."""


def setup_metric(metric: BaseMetric | dict) -> BaseMetric:
    r"""Set up the metric.

    Args:
        metric: The metric or its configuration.

    Returns:
        The instantiated metric.
    """
    if isinstance(metric, dict):
        logger.info("Initializing a metric from its configuration...")
        check_objectory()
        metric = BaseMetric.factory(**metric)
    if not isinstance(metric, Module):
        logger.warning(f"metric is not a 'torch.nn.Module' (received: {type(metric)})")
    return metric
