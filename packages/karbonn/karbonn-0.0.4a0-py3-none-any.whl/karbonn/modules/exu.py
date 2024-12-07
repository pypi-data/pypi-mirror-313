r"""Contain the exp-centered (ExU) layer."""

from __future__ import annotations

__all__ = ["ExU"]


import torch
from torch import Tensor, nn
from torch.nn import Parameter, functional
from torch.nn.init import trunc_normal_, zeros_


class ExU(nn.Module):
    r"""Implementation of the exp-centered (ExU) layer.

    This layer was proposed in the following paper:

        Neural Additive Models: Interpretable Machine Learning with
        Neural Nets.
        Agarwal R., Melnick L., Frosst N., Zhang X., Lengerich B.,
        Caruana R., Hinton G.
        NeurIPS 2021. (https://arxiv.org/pdf/2004.13912.pdf)

    Args:
        in_features: The size of each input sample.
        out_features: The size of each output sample.
        bias: If set to ``False``, the layer will not learn an
            additive bias.
        device: The device where to initialize the layer's parameters.
        dtype: The data type of the layer's parameters.

    Shape:
        - Input: ``(*, in_features)``, where ``*`` means any number of
            dimensions, including none.
        - Output: ``(*, out_features)``, where ``*`` is the same shape
            as the input.

    Example usage:

    ```pycon
    >>> import torch
    >>> from karbonn.modules import ExU
    >>> m = ExU(4, 6)
    >>> m
    ExU(in_features=4, out_features=6, bias=True)
    >>> out = m(torch.rand(6, 4))
    >>> out
    tensor([[...]], grad_fn=<MmBackward0>)

    ```
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = True,
        device: torch.device | None = None,
        dtype: torch.dtype | None = None,
    ) -> None:
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(torch.empty((out_features, in_features), **factory_kwargs))
        if bias:
            self.bias = Parameter(torch.empty(in_features, **factory_kwargs))
        else:
            self.register_parameter("bias", None)
        self.reset_parameters()

    def extra_repr(self) -> str:
        return f"in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}"

    def forward(self, input: Tensor) -> Tensor:  # noqa: A002
        x = input if self.bias is None else input.add(self.bias)
        return functional.linear(x, self.weight.exp())

    def reset_parameters(self) -> None:
        r"""Reset the parameters.

        As indicated in page 4 of the paper, the weights are initialed
        using a normal distribution ``N(4.0; 0.5)``. The biases are
        initialized to ``0``
        """
        mean, std = 4.0, 0.5
        trunc_normal_(self.weight, mean=mean, std=std, a=mean - 3 * std, b=mean + 3 * std)
        if self.bias is not None:
            zeros_(self.bias)
