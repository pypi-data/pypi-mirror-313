r"""Contain functional implementation of some activation layers."""

from __future__ import annotations

__all__ = ["safe_exp", "safe_log"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch


def safe_exp(input: torch.Tensor, max: float = 20.0) -> torch.Tensor:  # noqa: A002
    r"""Compute safely the exponential of the elements.

    The values that are higher than the specified minimum value are
    set to this maximum value. Using a not too large positive value
    leads to an output tensor without Inf.

    Args:
        input: The input tensor.
        max: The maximum value.

    Returns:
        A tensor with the exponential of the elements.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import safe_exp
    >>> output = safe_exp(torch.tensor([1.0, 10.0, 100.0, 1000.0]))
    >>> output
    tensor([2.7183e+00, 2.2026e+04, 4.8517e+08, 4.8517e+08])

    ```
    """
    return input.clamp(max=max).exp()


def safe_log(input: torch.Tensor, min: float = 1e-8) -> torch.Tensor:  # noqa: A002
    r"""Compute safely the logarithm natural logarithm of the elements.

    The values that are lower than the specified minimum value are set
    to this minimum value. Using a small positive value leads to an
    output tensor without NaN or Inf.

    Args:
        input: The input tensor.
        min: The minimum value.

    Returns:
        A tensor with the natural logarithm of the elements.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import safe_log
    >>> safe_log(torch.tensor([1e-4, 1e-5, 1e-6, 1e-8, 1e-9, 1e-10]))
    tensor([ -9.2103, -11.5129, -13.8155, -18.4207, -18.4207, -18.4207])

    ```
    """
    return input.clamp(min=min).log()
