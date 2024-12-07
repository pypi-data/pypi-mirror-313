r"""Contain a class to represent a buffer of tensors."""

from __future__ import annotations

__all__ = ["FlattenBuffer"]

from typing import Any

import torch
from coola.utils import str_indent
from torch import Tensor

from karbonn.distributed.ddp import all_gather_tensor_varshape


class FlattenBuffer:
    r"""Implement a class to represent a buffer of tensors.

    The tensors are flatten before to be concatenated.
    To be more efficient, the tensors are concatenated only when the
    method ``consolidate`` is called, i.e. the tensors are
    concatenated in a lazy way. The tensors are stored in an
    internal buffer, then they are concatenated and stored in a
    separate variable. Storing the result in a separate variable
    leads to a more efficient design because the tensor is generated
    only one time. Adding another tensor creates to a new tensor when
    the method ``consolidate`` is called.

    This class is at a very early stage and is very likely to change
    a lot in the future.

    Args:
        values: The initial values. The tensor is flattened if necessary.
            ``None`` means no initial values. Default: ``None``

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.tensor import FlattenBuffer
    >>> buffer = FlattenBuffer()
    >>> buffer.update(torch.arange(6))
    >>> buffer.update(torch.tensor([-3, 1, 7]))
    >>> buffer.values()
    tensor([ 0,  1,  2,  3,  4,  5, -3,  1,  7])
    >>> buffer.update(torch.arange(3))
    >>> buffer.values()
    tensor([ 0,  1,  2,  3,  4,  5, -3,  1,  7,  0,  1,  2])
    >>> # By default, the tensor type is torch.float32. To use another type like long,
    >>> # you need to specify the target type when creating the FlattenBuffer object.
    >>> buffer = FlattenBuffer(torch.tensor([], dtype=torch.long))
    >>> buffer.update(torch.arange(6))

    ```
    """

    def __init__(self, values: Tensor | None = None) -> None:
        if values is None:
            values = torch.tensor([])
        self._values = values.flatten()
        self._buffer = []

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(\n"
            f"  values={str_indent(self._values)}\n"
            f"  buffer={str_indent(self._buffer)}\n)"
        )

    def all_reduce(self) -> FlattenBuffer:
        r"""Reduce the values across all machines in such a way that all
        get the all the values.

        Returns:
            The reduced flatted tensor.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer()
        >>> buffer.update(torch.arange(6))
        >>> buffer_reduced = buffer.all_reduce()

        ```
        """
        return FlattenBuffer(torch.cat(all_gather_tensor_varshape(self.values()), dim=0))

    def clear(self) -> None:
        r"""Clear the values and the internal buffer.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer()
        >>> buffer.update(torch.arange(6))
        >>> buffer.clear()
        >>> buffer.values()
        tensor([])

        ```
        """
        self._values = torch.tensor([])
        self._buffer.clear()

    def clone(self) -> FlattenBuffer:
        r"""Create a copy of the current buffer.

        Returns:
            A copy of the current buffer.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer(torch.arange(6))
        >>> buffer_cloned = buffer.clone()
        >>> buffer.update(torch.ones(3))
        >>> buffer.values()
        tensor([0., 1., 2., 3., 4., 5., 1., 1., 1.])
        >>> buffer_cloned.values()
        tensor([0, 1, 2, 3, 4, 5])

        ```
        """
        return FlattenBuffer(self.values().clone())

    def consolidate(self) -> None:
        r"""Consolidate the current values and internal buffer in a
        single flatted tensor.

        This method does nothing if the buffer is already consolidated.
        """
        if self._buffer:
            values = self._values
            if values.numel() == 0:
                # Use the first tensor in the buffer to find the initial data type.
                values = values.to(dtype=self._buffer[0].dtype)
            self._values = torch.cat(
                [values] + [tensor.flatten() for tensor in self._buffer],
                dim=0,
            )
            self._buffer.clear()

    def equal(self, other: Any) -> bool:
        r"""Indicate if two objects are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the two objects are equal, ``False`` otherwise.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer1 = FlattenBuffer(torch.arange(6))
        >>> buffer2 = FlattenBuffer(torch.ones(3))
        >>> buffer1.equal(buffer2)
        False

        ```
        """
        if not isinstance(other, FlattenBuffer):
            return False
        if self.values().dtype != other.values().dtype:
            return False
        return self.values().equal(other.values())

    def numel(self) -> int:
        r"""Get the total number of elements.

        Returns:
            The total number of elements.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer(torch.arange(6))
        >>> buffer.numel()
        6

        ```
        """
        return self._values.numel() + sum(tensor.numel() for tensor in self._buffer)

    def update(self, tensor: Tensor) -> None:
        r"""Update the internal buffer by adding a new tensor.

        Args:
            tensor: The new tensor to add to the internal buffer.
                The tensor is flatted if necessary.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer()
        >>> buffer.update(torch.arange(6))
        >>> buffer.values()
        tensor([0, 1, 2, 3, 4, 5])

        ```
        """
        self._buffer.append(tensor)

    def values(self) -> Tensor:
        r"""Get a flatted tensor with all the values.

        Returns:
            The flatted tensor with all the values.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.tensor import FlattenBuffer
        >>> buffer = FlattenBuffer(torch.arange(6))
        >>> buffer.values()
        tensor([0, 1, 2, 3, 4, 5])

        ```
        """
        self.consolidate()
        return self._values
