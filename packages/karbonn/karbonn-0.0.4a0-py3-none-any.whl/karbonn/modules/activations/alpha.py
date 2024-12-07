r"""Contain activation layers with a learnable parameter ``alpha``."""

from __future__ import annotations

__all__ = [
    "BaseAlphaActivation",
    "ExpSin",
    "Gaussian",
    "Laplacian",
    "MultiQuadratic",
    "Quadratic",
]

import torch
from torch.nn import Module, Parameter


class BaseAlphaActivation(Module):
    r"""Define a base class to implement an activation layer with a
    learnable parameter ``alpha``.

    When called without arguments, the activation layer uses a single
    parameter ``alpha`` across all input channels. If called with a
    first argument, a separate ``alpha`` is used for each input
    channel.

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import MultiQuadratic
    >>> m = MultiQuadratic()
    >>> m
    MultiQuadratic(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000, 0.7071, 0.4472, 0.3162],
            [0.2425, 0.1961, 0.1644, 0.1414]], grad_fn=<MulBackward0>)

    ```
    """

    def __init__(self, num_parameters: int = 1, init: float = 1.0, learnable: bool = True) -> None:
        super().__init__()
        self.alpha = Parameter(
            torch.full((num_parameters,), init, dtype=torch.float), requires_grad=learnable
        )

    def extra_repr(self) -> str:
        return f"num_parameters={self.alpha.numel()}, learnable={self.alpha.requires_grad}"


class ExpSin(BaseAlphaActivation):
    r"""Implement the ExpSin activation layer.

    Formula: ``exp(-sin(alpha * x))``

    This activation layer was proposed in the following paper:

        Beyond Periodicity: Towards a Unifying Framework for Activations in Coordinate-MLPs.
        Ramasinghe S., Lucey S.
        ECCV 2022. (http://arxiv.org/pdf/2111.15135)

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import ExpSin
    >>> m = ExpSin()
    >>> m
    ExpSin(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000, 2.3198, 2.4826, 1.1516],
            [0.4692, 0.3833, 0.7562, 1.9290]], grad_fn=<ExpBackward0>)

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.mul(self.alpha).sin().exp()


class Gaussian(BaseAlphaActivation):
    r"""Implement the Gaussian activation layer.

    Formula: ``exp(-0.5 * x^2 / alpha^2)``

    This activation layer was proposed in the following paper:

        Beyond Periodicity: Towards a Unifying Framework for Activations in Coordinate-MLPs.
        Ramasinghe S., Lucey S.
        ECCV 2022. (http://arxiv.org/pdf/2111.15135)

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import Gaussian
    >>> m = Gaussian()
    >>> m
    Gaussian(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000e+00, 6.0653e-01, 1.3534e-01, 1.1109e-02],
            [3.3546e-04, 3.7267e-06, 1.5230e-08, 2.2897e-11]], grad_fn=<ExpBackward0>)

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.pow(2).mul(-0.5).div(self.alpha.pow(2)).exp()


class Laplacian(BaseAlphaActivation):
    r"""Implement the Laplacian activation layer.

    Formula: ``exp(-|x| / alpha)``

    This activation layer was proposed in the following paper:

        Beyond Periodicity: Towards a Unifying Framework for Activations in Coordinate-MLPs.
        Ramasinghe S., Lucey S.
        ECCV 2022. (http://arxiv.org/pdf/2111.15135)

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import Laplacian
    >>> m = Laplacian()
    >>> m
    Laplacian(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000e+00, 3.6788e-01, 1.3534e-01, 4.9787e-02],
            [1.8316e-02, 6.7379e-03, 2.4788e-03, 9.1188e-04]], grad_fn=<ExpBackward0>)

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return input.abs().mul(-1).div(self.alpha).exp()


class MultiQuadratic(BaseAlphaActivation):
    r"""Implement the Multi Quadratic activation layer.

    Formula: ``1 / sqrt(1 + (alpha * x)^2)``

    This activation layer was proposed in the following paper:

        Beyond Periodicity: Towards a Unifying Framework for Activations in Coordinate-MLPs.
        Ramasinghe S., Lucey S.
        ECCV 2022. (http://arxiv.org/pdf/2111.15135)

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import MultiQuadratic
    >>> m = MultiQuadratic()
    >>> m
    MultiQuadratic(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000, 0.7071, 0.4472, 0.3162],
            [0.2425, 0.1961, 0.1644, 0.1414]], grad_fn=<MulBackward0>)

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return 1.0 / input.mul(self.alpha).pow(2).add(1).sqrt()


class Quadratic(BaseAlphaActivation):
    r"""Implement the Quadratic activation layer.

    Formula: ``1 / (1 + (alpha * x)^2)``

    This activation layer was proposed in the following paper:

        Beyond Periodicity: Towards a Unifying Framework for Activations in Coordinate-MLPs.
        Ramasinghe S., Lucey S.
        ECCV 2022. (http://arxiv.org/pdf/2111.15135)

    Args:
        num_parameters: The number of learnable parameters. Although
            it takes an integer as input, there is only two values are
            legitimate: ``1``, or the number of channels at input.
        init: The initial value of the learnable parameter(s).
        learnable: If ``True``, the parameters are learnt during the
            training, otherwise they are fixed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Output: ``(*)``, same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import Quadratic
    >>> m = Quadratic()
    >>> m
    Quadratic(num_parameters=1, learnable=True)
    >>> out = m(torch.arange(8, dtype=torch.float).view(2, 4))
    >>> out
    tensor([[1.0000, 0.5000, 0.2000, 0.1000],
            [0.0588, 0.0385, 0.0270, 0.0200]], grad_fn=<MulBackward0>)

    ```
    """

    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        return 1.0 / input.mul(self.alpha).pow(2).add(1)
