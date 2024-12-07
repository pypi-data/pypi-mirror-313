r"""Contain the Poly1Loss implementation."""

from __future__ import annotations

__all__ = ["BinaryPoly1Loss", "BinaryPoly1LossWithLogits"]

import torch
from torch import nn

from karbonn.functional import (
    binary_poly1_loss,
    binary_poly1_loss_with_logits,
    check_loss_reduction_strategy,
)


class BinaryPoly1Loss(nn.Module):
    r"""Implementation of the binary Poly-1 loss for binary targets.

    Based on "PolyLoss: A Polynomial Expansion Perspective of
    Classification Loss Functions"
    (https://arxiv.org/pdf/2204.12511)

    Args:
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        gamma: The focusing parameter, which must be positive
            (``>=0``).
        reduction: The reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum of the output will be divided by the number of
            elements in the output, ``'sum'``: the output will be
            summed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Target: ``(*)``, same shape as the input.
        - Output: scalar. If ``reduction`` is ``'none'``, then ``(*)``,
            same shape as input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import BinaryPoly1Loss
    >>> criterion = BinaryPoly1Loss()
    >>> criterion
    BinaryPoly1Loss(alpha=1.0, reduction=mean)
    >>> prediction = torch.rand(2, 4, requires_grad=True)
    >>> target = torch.tensor([[1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0]])
    >>> loss = criterion(prediction, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, alpha: float = 1.0, reduction: str = "mean") -> None:
        super().__init__()
        self._alpha = float(alpha)

        check_loss_reduction_strategy(reduction)
        self.reduction = reduction

    def extra_repr(self) -> str:
        return f"alpha={self._alpha}, reduction={self.reduction}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        r"""Compute the binary Poly-1 loss for binary targets.

        Args:
            prediction: The float tensor with predictions as
                probabilities for each example.
            target: A float tensor with the same shape as inputs.
                It stores the binary classification label for each
                element in inputs (0 for the negative class and 1 for
                the positive class).

        Returns:
            The loss value(s). The shape of the tensor depends on the
                reduction. If the reduction is ``mean`` or ``sum``,
                the tensor has a single scalar value. If the reduction
                is ``none``, the shape of the tensor is the same as
                the inputs.
        """
        return binary_poly1_loss(
            prediction=prediction,
            target=target,
            alpha=self._alpha,
            reduction=self.reduction,
        )


class BinaryPoly1LossWithLogits(nn.Module):
    r"""Implementation of the binary Poly-1 loss for binary targets.

    Based on "PolyLoss: A Polynomial Expansion Perspective of
    Classification Loss Functions"
    (https://arxiv.org/pdf/2204.12511)

    Args:
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        gamma: The focusing parameter, which must be positive
            (``>=0``).
        reduction: The reduction to apply to the output:
            ``'none'`` | ``'mean'`` | ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum of the output will be divided by the number of
            elements in the output, ``'sum'``: the output will be
            summed.

    Shape:
        - Input: ``(*)``, where ``*`` means any number of dimensions.
        - Target: ``(*)``, same shape as the input.
        - Output: scalar. If ``reduction`` is ``'none'``, then ``(*)``,
            same shape as input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import BinaryPoly1LossWithLogits
    >>> criterion = BinaryPoly1LossWithLogits()
    >>> criterion
    BinaryPoly1LossWithLogits(alpha=1.0, reduction=mean)
    >>> prediction = torch.randn(2, 4, requires_grad=True)
    >>> target = torch.tensor([[1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0]])
    >>> loss = criterion(prediction, target)
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(self, alpha: float = 1.0, reduction: str = "mean") -> None:
        super().__init__()
        self._alpha = float(alpha)

        check_loss_reduction_strategy(reduction)
        self.reduction = reduction

    def extra_repr(self) -> str:
        return f"alpha={self._alpha}, reduction={self.reduction}"

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        r"""Compute the binary Poly-1 loss for binary targets.

        Args:
            prediction: The float tensor with predictions as
                unnormalized scores (often referred to as logits) for
                each example.
            target: A float tensor with the same shape as inputs.
                It stores the binary classification label for each
                element in inputs (0 for the negative class and 1 for
                the positive class).

        Returns:
            The loss value(s). The shape of the tensor depends on the
                reduction. If the reduction is ``mean`` or ``sum``,
                the tensor has a single scalar value. If the reduction
                is ``none``, the shape of the tensor is the same as
                the inputs.
        """
        return binary_poly1_loss_with_logits(
            prediction=prediction,
            target=target,
            alpha=self._alpha,
            reduction=self.reduction,
        )
