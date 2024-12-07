r"""Contain relative indicator functions."""

from __future__ import annotations

__all__ = [
    "ArithmeticalMeanIndicator",
    "BaseRelativeIndicator",
    "ClassicalRelativeIndicator",
    "GeometricMeanIndicator",
    "MaximumMeanIndicator",
    "MinimumMeanIndicator",
    "MomentMeanIndicator",
    "ReversedRelativeIndicator",
]


import torch
from torch import nn

from karbonn.functional.loss.relative import (
    arithmetical_mean_indicator,
    classical_relative_indicator,
    geometric_mean_indicator,
    maximum_mean_indicator,
    minimum_mean_indicator,
    moment_mean_indicator,
    reversed_relative_indicator,
)


class BaseRelativeIndicator(nn.Module):
    r"""Define the base class to implement a relative indicator function.

    The indicators are designed based on
    https://en.wikipedia.org/wiki/Relative_change#Indicators_of_relative_change.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import ClassicalRelativeIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = ClassicalRelativeIndicator()
    >>> indicator
    ClassicalRelativeIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[2., 1., 0.],
            [3., 5., 1.]])

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        r"""Return the indicator values.

        Args:
            prediction: The predictions.
            target: The target values.

        Returns:
            The indicator values.
        """


class ArithmeticalMeanIndicator(BaseRelativeIndicator):
    r"""Implement the arithmetical mean change indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import ArithmeticalMeanIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = ArithmeticalMeanIndicator()
    >>> indicator
    ArithmeticalMeanIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[1.0000, 1.0000, 0.5000],
            [3.0000, 3.0000, 1.0000]], grad_fn=<MulBackward0>)

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return arithmetical_mean_indicator(prediction, target)


class ClassicalRelativeIndicator(BaseRelativeIndicator):
    r"""Implement the classical relative indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import ClassicalRelativeIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = ClassicalRelativeIndicator()
    >>> indicator
    ClassicalRelativeIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[2., 1., 0.],
            [3., 5., 1.]])

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return classical_relative_indicator(prediction, target)


class GeometricMeanIndicator(BaseRelativeIndicator):
    r"""Implement the geometric mean indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import GeometricMeanIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = GeometricMeanIndicator()
    >>> indicator
    GeometricMeanIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[0.0000, 1.0000, 0.0000],
            [3.0000, 2.2361, 1.0000]], grad_fn=<SqrtBackward0>)

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return geometric_mean_indicator(prediction, target)


class MaximumMeanIndicator(BaseRelativeIndicator):
    r"""Implement the maximum mean change indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import MaximumMeanIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = MaximumMeanIndicator()
    >>> indicator
    MaximumMeanIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[2., 1., 1.],
            [3., 5., 1.]], grad_fn=<MaximumBackward0>)

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return maximum_mean_indicator(prediction, target)


class MinimumMeanIndicator(BaseRelativeIndicator):
    r"""Implement the minimum mean change indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import MinimumMeanIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = MinimumMeanIndicator()
    >>> indicator
    MinimumMeanIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[0., 1., 0.],
            [3., 1., 1.]], grad_fn=<MinimumBackward0>)

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return minimum_mean_indicator(prediction, target)


class MomentMeanIndicator(BaseRelativeIndicator):
    r"""Implement the moment mean change of order k indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import MomentMeanIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = MomentMeanIndicator()
    >>> indicator
    MomentMeanIndicator(k=1)
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[1.0000, 1.0000, 0.5000],
            [3.0000, 3.0000, 1.0000]], grad_fn=<PowBackward0>)

    ```
    """

    def __init__(self, k: int = 1) -> None:
        super().__init__()
        self._k = k

    def extra_repr(self) -> str:
        return f"k={self._k}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return moment_mean_indicator(prediction, target, k=self._k)


class ReversedRelativeIndicator(BaseRelativeIndicator):
    r"""Implement the reversed relative indicator function.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules.loss import ReversedRelativeIndicator
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> indicator = ReversedRelativeIndicator()
    >>> indicator
    ReversedRelativeIndicator()
    >>> values = indicator(
    ...     prediction=torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True),
    ...     target=torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]]),
    ... )
    >>> values
    tensor([[0., 1., 1.],
            [3., 1., 1.]], grad_fn=<AbsBackward0>)

    ```
    """

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return reversed_relative_indicator(prediction, target)
