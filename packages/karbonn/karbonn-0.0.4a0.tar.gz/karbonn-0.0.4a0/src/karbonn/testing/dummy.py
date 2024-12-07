r"""Contain testing/debugging modules."""

from __future__ import annotations

__all__ = ["DummyDataset"]

import torch
from torch.utils.data import Dataset

from karbonn.utils.seed import get_torch_generator


class DummyDataset(Dataset):
    r"""Implement a dummy map-style dataset for testing purpose.

    Args:
        feature_size: The feature size.
        num_examples: The number of examples.

    Example usage:

    ```pycon

    >>> from karbonn.testing.dummy import DummyDataset
    >>> dataset = DummyDataset(num_examples=10, feature_size=7)
    >>> dataset[0]
    {'feature': tensor([...]), 'target': tensor([...])}

    ```
    """

    def __init__(
        self, feature_size: int = 4, num_examples: int = 8, rng_seed: int = 14700295087918620795
    ) -> None:
        self._feature_size = int(feature_size)
        self._num_examples = int(num_examples)
        self._rng_seed = rng_seed

        self._features = torch.randn(
            num_examples, feature_size, generator=get_torch_generator(rng_seed)
        )
        self._target = 0.6 * self._features[:, :1] + 0.4 * self._features[:, -1:]

    def __getitem__(self, item: int) -> dict:
        return {"feature": self._features[item], "target": self._target[item]}

    def __len__(self) -> int:
        return self._num_examples

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(num_examples={self._num_examples:,}, "
            f"feature_size={self._feature_size:,}, rng_seed={self._rng_seed})"
        )
