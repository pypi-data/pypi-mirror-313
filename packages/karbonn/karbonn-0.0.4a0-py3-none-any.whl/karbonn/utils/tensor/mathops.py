r"""Contain some math utility functions."""

from __future__ import annotations

__all__ = ["quantile", "quantile_numpy"]

from unittest.mock import Mock

import torch
from coola.utils.imports import check_torch_numpy, is_numpy_available
from torch import Tensor

if is_numpy_available():
    import numpy as np
else:  # pragma: no cover
    np = Mock()


def quantile(
    tensor: Tensor, q: float | Tensor, dim: int | None = None, *, interpolation: str = "linear"
) -> Tensor:
    r"""Return the ``q``-th quantiles.

    This function uses numpy to compute the ``q``-th quantiles
    if the tensor has more than 16M items because PyTorch has a
    limit to 16M items.
    https://github.com/pytorch/pytorch/issues/64947

    Args:
        tensor: The tensor of values.
        q: The ``q``-values in the range ``[0, 1]``. This input is a
            ``torch.Tensor`` of type float and shape
            ``(num_q_values,)``.
        dim: The dimension to reduce.
        interpolation: The interpolation method to use when the desired
            quantile lies between two data points. Can be
            ``'linear'``, ``'lower'``, ``'higher'``, ``'midpoint'``
            and ``'nearest'``.

    Returns:
        The ``q``-th quantiles as a ``torch.Tensor`` of shape
            ``(num_q_values,)``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.tensor import quantile
    >>> quantile(torch.arange(101, dtype=torch.float), q=torch.tensor([0.1, 0.9]))
    tensor([10., 90.])

    ```
    """
    if tensor.numel() < 16e6:
        return torch.quantile(tensor, q=q, dim=dim, interpolation=interpolation)
    return quantile_numpy(tensor=tensor, q=q, dim=dim, interpolation=interpolation)


def quantile_numpy(
    tensor: Tensor, q: float | Tensor, dim: int | None = None, *, interpolation: str = "linear"
) -> torch.Tensor:
    r"""Return the ``q``-th quantiles.

    This function uses numpy to compute the ``q``-th quantiles
    because PyTorch has a limit to 16M items.
    https://github.com/pytorch/pytorch/issues/64947

    Args:
        tensor: The tensor of values.
        q: The ``q``-values in the range ``[0, 1]``. This input is a
            ``torch.Tensor`` of type float and shape
            ``(num_q_values,)``.
        dim: The dimension to reduce.
        interpolation: The interpolation method to use when the desired
            quantile lies between two data points. Can be
            ``'linear'``, ``'lower'``, ``'higher'``, ``'midpoint'``
            and ``'nearest'``.

    Returns:
        The ``q``-th quantiles as a ``torch.Tensor`` of shape
            ``(num_q_values,)``.

    Raises:
        RuntimeError: if ``numpy`` is not installed or not compatible
            with ``torch``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.tensor import quantile_numpy
    >>> quantile_numpy(torch.arange(101, dtype=torch.float), q=torch.tensor([0.1, 0.9]))
    tensor([10., 90.])

    ```
    """
    check_torch_numpy()
    return torch.from_numpy(
        np.quantile(
            tensor.detach().cpu().numpy(),
            q=q.detach().cpu().numpy() if torch.is_tensor(q) else q,
            axis=dim,
            method=interpolation,
        )
    ).to(dtype=tensor.dtype, device=tensor.device)
