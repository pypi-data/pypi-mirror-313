r"""Contain relative loss functions."""

from __future__ import annotations

__all__ = [
    "arithmetical_mean_indicator",
    "classical_relative_indicator",
    "geometric_mean_indicator",
    "maximum_mean_indicator",
    "minimum_mean_indicator",
    "moment_mean_indicator",
    "relative_loss",
    "reversed_relative_indicator",
]


import torch

from karbonn.functional.reduction import reduce_loss


def relative_loss(
    loss: torch.Tensor,
    indicator: torch.Tensor,
    reduction: str = "mean",
    eps: float = 1e-8,
) -> torch.Tensor:
    r"""Compute the relative loss.

    The indicators are designed based on
    https://en.wikipedia.org/wiki/Relative_change#Indicators_of_relative_change.

    Args:
        loss: The loss values. The tensor must have the same shape as
            the target.
        indicator: The indicator values.
        reduction: The reduction strategy. The valid values are
            ``'mean'``, ``'none'``,  and ``'sum'``.
            ``'none'``: no reduction will be applied, ``'mean'``: the
            sum will be divided by the number of elements in the
            input, ``'sum'``: the output will be summed.
        eps: An arbitrary small strictly positive number to avoid
            undefined results when the indicator is zero.

    Returns:
        The computed relative loss.

    Raises:
        RuntimeError: if the loss and indicator shapes do not match.
        ValueError: if the reduction is not valid.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional import relative_loss
    >>> prediction = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> loss = relative_loss(
    ...     loss=torch.nn.functional.mse_loss(prediction, target, reduction="none"),
    ...     indicator=classical_relative_indicator(prediction, target),
    ... )
    >>> loss
    tensor(..., grad_fn=<MeanBackward0>)
    >>> loss.backward()

    ```
    """
    if loss.shape != indicator.shape:
        msg = f"loss {loss.shape} and indicator {indicator.shape} shapes do not match"
        raise RuntimeError(msg)
    return reduce_loss(loss.div(indicator.clamp(min=eps)), reduction)


def arithmetical_mean_indicator(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    r"""Return the arithmetical mean change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import arithmetical_mean_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = arithmetical_mean_indicator(prediction, target)
    >>> indicator
    tensor([[1.0000, 1.0000, 0.5000],
            [3.0000, 3.0000, 1.0000]], grad_fn=<MulBackward0>)

    ```
    """
    return target.abs().add(prediction.abs()).mul(0.5)


def classical_relative_indicator(
    prediction: torch.Tensor,  # noqa: ARG001
    target: torch.Tensor,
) -> torch.Tensor:
    r"""Return the classical relative change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import classical_relative_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = classical_relative_indicator(prediction, target)
    >>> indicator
    tensor([[2., 1., 0.],
            [3., 5., 1.]])

    ```
    """
    return target.abs()


def geometric_mean_indicator(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    r"""Return the geometric mean change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import geometric_mean_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = geometric_mean_indicator(prediction, target)
    >>> indicator
    tensor([[0.0000, 1.0000, 0.0000],
            [3.0000, 2.2361, 1.0000]], grad_fn=<SqrtBackward0>)

    ```
    """
    return target.abs().mul(prediction.abs()).sqrt()


def maximum_mean_indicator(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    r"""Return the maximum mean change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import maximum_mean_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = maximum_mean_indicator(prediction, target)
    >>> indicator
    tensor([[2., 1., 1.],
            [3., 5., 1.]], grad_fn=<MaximumBackward0>)

    ```
    """
    return torch.maximum(target.abs(), prediction.abs())


def minimum_mean_indicator(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    r"""Return the minimum mean change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import minimum_mean_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = minimum_mean_indicator(prediction, target)
    >>> indicator
    tensor([[0., 1., 0.],
            [3., 1., 1.]], grad_fn=<MinimumBackward0>)

    ```
    """
    return torch.minimum(target.abs(), prediction.abs())


def moment_mean_indicator(
    prediction: torch.Tensor, target: torch.Tensor, k: int = 1
) -> torch.Tensor:
    r"""Return the moment mean change of order k.

    Args:
        prediction: The predictions.
        target: The target values.
        k:  The order.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import moment_mean_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = moment_mean_indicator(prediction, target)
    >>> indicator
    tensor([[1.0000, 1.0000, 0.5000],
            [3.0000, 3.0000, 1.0000]], grad_fn=<PowBackward0>)

    ```
    """
    return target.abs().pow(k).add(prediction.abs().pow(k)).mul(0.5).pow(1 / k)


def reversed_relative_indicator(
    prediction: torch.Tensor,
    target: torch.Tensor,  # noqa: ARG001
) -> torch.Tensor:
    r"""Return the reversed relative change.

    Args:
        prediction: The predictions.
        target: The target values.

    Returns:
        The indicator values.

    ```pycon

    >>> import torch
    >>> from karbonn.functional.loss import reversed_relative_indicator
    >>> prediction = torch.tensor([[0.0, 1.0, -1.0], [3.0, 1.0, -1.0]], requires_grad=True)
    >>> target = torch.tensor([[-2.0, 1.0, 0.0], [-3.0, 5.0, -1.0]])
    >>> indicator = reversed_relative_indicator(prediction, target)
    >>> indicator
    tensor([[0., 1., 1.],
            [3., 1., 1.]], grad_fn=<AbsBackward0>)

    ```
    """
    return prediction.abs()
