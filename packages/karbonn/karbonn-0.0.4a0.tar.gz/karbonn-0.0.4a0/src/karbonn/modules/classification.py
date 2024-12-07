r"""Contain the classification specific layers."""

from __future__ import annotations

__all__ = ["ToBinaryLabel", "ToCategoricalLabel"]

import torch
from torch import nn


class ToBinaryLabel(nn.Module):
    r"""Implement a ``torch.nn.Module`` to compute binary labels from
    scores by thresholding.

    The output label is ``1`` if the value is greater than the
    threshold, and ``0`` otherwise.

    Args:
        threshold: The threshold value used to compute the binary
            labels.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import ToBinaryLabel
    >>> transform = ToBinaryLabel()
    >>> transform
    ToBinaryLabel(threshold=0.0)
    >>> out = transform(torch.tensor([-1.0, 1.0, -2.0, 1.0]))
    >>> out
    tensor([0, 1, 0, 1])

    ```
    """

    def __init__(self, threshold: float = 0.0) -> None:
        super().__init__()
        self._threshold = float(threshold)

    @property
    def threshold(self) -> float:
        r"""The threshold used to compute the binary label."""
        return self._threshold

    def extra_repr(self) -> str:
        return f"threshold={self._threshold}"

    def forward(self, scores: torch.Tensor) -> torch.Tensor:
        r"""Compute binary labels from scores.

        Args:
            scores: The scores used to compute the binary labels.
                This input must be a ``torch.Tensor`` of type float
                and shape ``(d0, d1, ..., dn)``

        Returns:
            The computed binary labels where the values are ``0`` and
                ``1``. The output is a ``torch.Tensor`` of type long
                and shape ``(d0, d1, ..., dn)``.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import ToBinaryLabel
        >>> transform = ToBinaryLabel()
        >>> out = transform(torch.tensor([-1.0, 1.0, -2.0, 1.0]))
        >>> out
        tensor([0, 1, 0, 1])

        ```
        """
        return (scores > self._threshold).long()


class ToCategoricalLabel(nn.Module):
    r"""Implement a ``torch.nn.Module`` to compute categorical labels
    from scores.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import ToCategoricalLabel
    >>> transform = ToCategoricalLabel()
    >>> transform
    ToCategoricalLabel()
    >>> out = transform(torch.tensor([[1.0, 2.0, 3.0, 4.0], [5.0, 3.0, 2.0, 2.0]]))
    >>> out
    tensor([3, 0])

    ```
    """

    def forward(self, scores: torch.Tensor) -> torch.Tensor:
        r"""Compute categorical labels from scores.

        Args:
            scores: The scores used to compute the categorical labels.
                This input must be a ``torch.Tensor`` of shape
                ``(d0, d1, ..., dn, num_classes)`` and type float.

        Returns:
            The computed categorical labels where the values are in
                ``{0, 1, ..., num_classes-1}``. The output is a
                ``torch.Tensor`` of type long and shape
                ``(d0, d1, ..., dn)``.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import ToCategoricalLabel
        >>> transform = ToCategoricalLabel()
        >>> out = transform(torch.tensor([[1.0, 2.0, 3.0, 4.0], [5.0, 3.0, 2.0, 2.0]]))
        >>> out
        tensor([3, 0])

        ```
        """
        return scores.argmax(dim=-1, keepdim=False)
