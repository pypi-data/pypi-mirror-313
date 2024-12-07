r"""Contain a simple dataset creator implementation."""

from __future__ import annotations

__all__ = ["DatasetCreator"]

from typing import TYPE_CHECKING, TypeVar

from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping

from karbonn.creator.dataset.base import BaseDatasetCreator
from karbonn.utils.factory import setup_dataset

if TYPE_CHECKING:
    from torch.utils.data import Dataset

T = TypeVar("T")


class DatasetCreator(BaseDatasetCreator[T]):
    r"""Implement a simple dataset creator.

    Args:
        dataset: The dataset or its configuration.

    Example usage:

    ```pycon

    >>> from karbonn.creator.dataset import DatasetCreator
    >>> creator = DatasetCreator(
    ...     {
    ...         "_target_": "karbonn.testing.dummy.DummyDataset",
    ...         "num_examples": 10,
    ...         "feature_size": 4,
    ...     }
    ... )
    >>> creator
    DatasetCreator(
      (_target_): karbonn.testing.dummy.DummyDataset
      (feature_size): 4
      (num_examples): 10
    )
    >>> creator.create()
    DummyDataset(num_examples=10, feature_size=4, rng_seed=14700295087918620795)

    ```
    """

    def __init__(self, dataset: Dataset[T] | dict) -> None:
        self._dataset = dataset

    def __repr__(self) -> str:
        config = (
            repr_mapping(self._dataset, sorted_keys=True)
            if isinstance(self._dataset, dict)
            else self._dataset
        )
        return f"{self.__class__.__qualname__}(\n  {repr_indent(config)}\n)"

    def __str__(self) -> str:
        config = (
            str_mapping(self._dataset, sorted_keys=True)
            if isinstance(self._dataset, dict)
            else self._dataset
        )
        return f"{self.__class__.__qualname__}(\n  {str_indent(config)}\n)"

    def create(self) -> Dataset[T]:
        return setup_dataset(self._dataset)
