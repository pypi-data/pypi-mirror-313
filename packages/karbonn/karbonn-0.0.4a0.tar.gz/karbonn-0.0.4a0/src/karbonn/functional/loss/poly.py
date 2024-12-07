r"""Contain the implementation of the PolyLoss function."""

from __future__ import annotations

__all__ = ["binary_poly1_loss", "binary_poly1_loss_with_logits"]


import torch
from torch.nn.functional import binary_cross_entropy, binary_cross_entropy_with_logits

from karbonn.functional.reduction import reduce_loss


def binary_poly1_loss(
    prediction: torch.Tensor,
    target: torch.Tensor,
    alpha: float = 1.0,
    reduction: str = "mean",
) -> torch.Tensor:
    r"""Compute the Poly-1 loss for binary targets.

    Based on "PolyLoss: A Polynomial Expansion Perspective of
    Classification Loss Functions"
    (https://arxiv.org/pdf/2204.12511)

    Args:
        prediction: The float tensor with predictions as probabilities
            for each example.
        target: A float tensor with the same shape as inputs. It stores
            the binary classification label for each element in inputs
            (0 for the negative class and 1 for the positive class).
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The computed Poly-1 loss value. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import binary_poly1_loss
    >>> loss = binary_poly1_loss(
    ...     torch.rand(2, 4, requires_grad=True),
    ...     torch.tensor([[1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0]]),
    ... )
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    ce_loss = binary_cross_entropy(prediction, target, reduction="none")
    p_t = prediction * target + (1 - prediction) * (1 - target)
    loss = ce_loss + alpha * (1 - p_t)
    return reduce_loss(loss, reduction)


def binary_poly1_loss_with_logits(
    prediction: torch.Tensor,
    target: torch.Tensor,
    alpha: float = 1.0,
    reduction: str = "mean",
) -> torch.Tensor:
    r"""Compute the Poly-1 loss.

    Based on "PolyLoss: A Polynomial Expansion Perspective of
    Classification Loss Functions"
    (https://arxiv.org/pdf/2204.12511)

    Args:
        prediction: The float tensor with predictions as unnormalized
            scores (often referred to as logits) for each example.
        target: A float tensor with the same shape as inputs. It stores
            the binary classification label for each element in inputs
            (0 for the negative class and 1 for the positive class).
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The computed Poly-1 loss value. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import binary_poly1_loss_with_logits
    >>> loss = binary_poly1_loss_with_logits(
    ...     torch.randn(2, 4, requires_grad=True),
    ...     torch.tensor([[1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0]]),
    ... )
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    p = torch.sigmoid(prediction)
    ce_loss = binary_cross_entropy_with_logits(prediction, target, reduction="none")
    p_t = p * target + (1 - p) * (1 - target)
    loss = ce_loss + alpha * (1 - p_t)
    return reduce_loss(loss, reduction)
