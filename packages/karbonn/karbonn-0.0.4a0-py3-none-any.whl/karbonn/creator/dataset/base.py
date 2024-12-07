r"""Contain the base class to implement a dataset creator."""

from __future__ import annotations

__all__ = ["BaseDatasetCreator", "is_dataset_creator_config", "setup_dataset_creator"]

import logging
from abc import abstractmethod
from typing import TypeVar
from unittest.mock import Mock

from torch.utils.data import Dataset

from karbonn.creator.base import BaseCreator
from karbonn.utils.factory import setup_object_typed
from karbonn.utils.imports import check_objectory, is_objectory_available

if is_objectory_available():
    import objectory
else:  # pragma: no cover
    objectory = Mock()


logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseDatasetCreator(BaseCreator[Dataset[T]]):
    r"""Define the base class to implement a dataset creator.

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

    @abstractmethod
    def create(self) -> Dataset[T]:
        r"""Create a dataset.

        Returns:
            The created dataset.

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
        >>> creator.create()
        DummyDataset(num_examples=10, feature_size=4, rng_seed=14700295087918620795)

        ```
        """


def is_dataset_creator_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseDatasetCreator``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseDatasetCreator`` object,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> from karbonn.creator.dataset import is_dataset_creator_config
    >>> is_dataset_creator_config(
    ...     {
    ...         "_target_": "karbonn.creator.dataset.DatasetCreator",
    ...         "dataset": {
    ...             "_target_": "karbonn.testing.dummy.DummyDataset",
    ...             "num_examples": 10,
    ...             "feature_size": 4,
    ...         },
    ...     }
    ... )
    True

    ```
    """
    check_objectory()
    return objectory.utils.is_object_config(config, BaseDatasetCreator)


def setup_dataset_creator(creator: BaseDatasetCreator | dict) -> BaseDatasetCreator:
    r"""Set up a ``BaseDatasetCreator`` object.

    Args:
        creator: The dataset creator or its configuration.

    Returns:
        The instantiated ``BaseDatasetCreator`` object.

    Example usage:

    ```pycon

    >>> from karbonn.creator.dataset import setup_dataset_creator
    >>> creator = setup_dataset_creator(
    ...     {
    ...         "_target_": "karbonn.creator.dataset.DatasetCreator",
    ...         "dataset": {
    ...             "_target_": "karbonn.testing.dummy.DummyDataset",
    ...             "num_examples": 10,
    ...             "feature_size": 4,
    ...         },
    ...     }
    ... )
    >>> creator
    DatasetCreator(
      (_target_): karbonn.testing.dummy.DummyDataset
      (feature_size): 4
      (num_examples): 10
    )

    ```
    """
    return setup_object_typed(
        obj_or_config=creator, cls=BaseDatasetCreator, name="BaseDatasetCreator"
    )
