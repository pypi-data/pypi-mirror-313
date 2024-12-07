r"""Contain the implementation of the focal loss function."""

from __future__ import annotations

__all__ = ["binary_focal_loss", "binary_focal_loss_with_logits"]


import torch
from torch.nn.functional import binary_cross_entropy, binary_cross_entropy_with_logits

from karbonn.functional.reduction import reduce_loss


def binary_focal_loss(
    prediction: torch.Tensor,
    target: torch.Tensor,
    alpha: float = 0.25,
    gamma: float = 2.0,
    reduction: str = "mean",
) -> torch.Tensor:
    r"""Compute the binary focal loss.

    Based on "Focal Loss for Dense Object Detection"
    (https://arxiv.org/pdf/1708.02002.pdf)
    Implementation is based on
    https://pytorch.org/vision/main/_modules/torchvision/ops/focal_loss.html

    Args:
        prediction: The float tensor with predictions as probabilities
            for each example.
        target: A float tensor with the same shape as inputs. It stores
            the binary classification label for each element in inputs
            (0 for the negative class and 1 for the positive class).
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        gamma: The focusing parameter, which must be positive
            (``>=0``).
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The computed binary focal loss. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import binary_focal_loss
    >>> loss = binary_focal_loss(
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
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * target + (1 - alpha) * (1 - target)
        loss = alpha_t * loss
    return reduce_loss(loss, reduction)


def binary_focal_loss_with_logits(
    prediction: torch.Tensor,
    target: torch.Tensor,
    alpha: float = 0.25,
    gamma: float = 2.0,
    reduction: str = "mean",
) -> torch.Tensor:
    r"""Compute the binary focal loss.

    Based on "Focal Loss for Dense Object Detection"
    (https://arxiv.org/pdf/1708.02002.pdf)
    Implementation is based on
    https://pytorch.org/vision/main/_modules/torchvision/ops/focal_loss.html

    Args:
        prediction: The float tensor with predictions as unnormalized
            scores (often referred to as logits) for each example.
        target: A float tensor with the same shape as inputs. It stores
            the binary classification label for each element in inputs
            (0 for the negative class and 1 for the positive class).
        alpha: The weighting factor, which must be in the range
            ``[0, 1]``. This parameter is ignored if negative.
        gamma: The focusing parameter, which must be positive
            (``>=0``).
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.

    Returns:
        The computed binary focal loss. The shape of the tensor depends
            on the reduction strategy.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import binary_focal_loss_with_logits
    >>> loss = binary_focal_loss_with_logits(
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
    loss = ce_loss * ((1 - p_t) ** gamma)

    if alpha >= 0:
        alpha_t = alpha * target + (1 - alpha) * (1 - target)
        loss = alpha_t * loss
    return reduce_loss(loss, reduction)
