r"""Contain modules to compute N separate linear layers."""

from __future__ import annotations

__all__ = ["NLinear"]

import math
from typing import TYPE_CHECKING

import torch.nn
from torch.nn import Module, Parameter, init

if TYPE_CHECKING:
    from torch import Tensor


class NLinear(Module):
    r"""Implement N separate linear layers.

    Technically, ``NLinear(n, in, out)`` is just a layout of ``n``
    linear layers ``torch.nn.Linear(in, out)``.

    Args:
        n: The number of separate linear layers.
        in_features: The size of each input sample.
        out_features: The size of each output sample.
        bias: If set to ``False``, the layer will not learn an
            additive bias.

    Shape:
        - Input: ``(*, n, in_features)``, where ``*`` means any number of
            dimensions.
        - Output: ``(*, n, out_features)``,  where ``*`` has
            the same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import NLinear
    >>> # Example with 1 feature
    >>> m = NLinear(n=3, in_features=4, out_features=6)
    >>> m
    NLinear(n=3, in_features=4, out_features=6, bias=True)
    >>> out = m(torch.randn(2, 3, 4))
    >>> out.shape
    torch.Size([2, 3, 6])
    >>> out = m(torch.randn(2, 5, 3, 4))
    >>> out.shape
    torch.Size([2, 5, 3, 6])

    ```
    """

    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        bias: bool = True,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> None:
        super().__init__()
        factory_kwargs = {"device": device, "dtype": dtype}
        self.weight = Parameter(torch.empty((n, in_features, out_features), **factory_kwargs))
        if bias:
            self.bias = Parameter(torch.empty(n, out_features, **factory_kwargs))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    @property
    def n(self) -> int:
        return self.weight.shape[0]

    @property
    def in_features(self) -> int:
        return self.weight.shape[1]

    @property
    def out_features(self) -> int:
        return self.weight.shape[2]

    def reset_parameters(self) -> None:
        # Setting a=sqrt(5) in kaiming_uniform is the same as initializing with
        # uniform(-1/sqrt(in_features), 1/sqrt(in_features)). For details, see
        # https://github.com/pytorch/pytorch/issues/57109
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor) -> Tensor:
        shape = x.shape
        x = x.view(-1, shape[-2], shape[-1]).transpose(0, 1)
        x @= self.weight
        x = x.transpose(0, 1).view(*shape[:-1], self.out_features)
        if self.bias is not None:
            x += self.bias
        return x

    def extra_repr(self) -> str:
        return (
            f"n={self.n}, in_features={self.in_features}, out_features={self.out_features}, "
            f"bias={self.bias is not None}"
        )
