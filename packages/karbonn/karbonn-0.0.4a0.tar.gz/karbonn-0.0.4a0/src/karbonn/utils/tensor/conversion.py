r"""Contain tensor conversion utility functions."""

from __future__ import annotations

__all__ = ["to_tensor"]

from collections.abc import Sequence
from typing import Any
from unittest.mock import Mock

import torch
from coola.utils import is_numpy_available

if is_numpy_available():
    import numpy as np
else:  # pragma: no cover
    np = Mock()


def to_tensor(data: Any) -> torch.Tensor:
    r"""Convert the input to a ``torch.Tensor``.

    Args:
        data: The data to convert to ``torch.Tensor``.

    Returns:
        The tensor.

    Raises:
        TypeError: if the type cannot be converted to ``torch.Tensor``.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import torch
    >>> from karbonn.utils.tensor import to_tensor
    >>> to_tensor(torch.tensor([-3, 1, 7]))
    tensor([-3,  1,  7])
    >>> to_tensor([-3, 1, 7])
    tensor([-3,  1,  7])
    >>> to_tensor((-3, 1, 7))
    tensor([-3,  1,  7])
    >>> to_tensor(np.array([-3, 1, 7]))
    tensor([-3,  1,  7])

    ```
    """
    if torch.is_tensor(data):
        return data
    if is_numpy_available() and isinstance(data, np.ndarray):
        return torch.from_numpy(data)
    if isinstance(data, (Sequence, int, float)):
        return torch.as_tensor(data)
    msg = f"Incorrect type: {type(data)}"
    raise TypeError(msg)
