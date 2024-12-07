r"""Contain a loss function where the predictions and targets are
transformed before to be fed to the loss function."""

from __future__ import annotations

__all__ = ["TransformedLoss"]

import torch
from torch import nn

from karbonn.utils import setup_module


class TransformedLoss(nn.Module):
    r"""Implement a loss function where the predictions and targets are
    transformed before to be fed to the loss function.

    Args:
        criterion: The criterion or its configuration. The loss has
            two inputs: predictions and targets.
        prediction: The transformation for the predictions or its
            configuration. If ``None``, the identity transformation
            is used.
        target: The transformation for the targets or its
            configuration. If ``None``, the identity transformation
            is used.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import TransformedLoss, Asinh
    >>> criterion = TransformedLoss(
    ...     criterion=torch.nn.SmoothL1Loss(),
    ...     prediction=Asinh(),
    ...     target=Asinh(),
    ... )
    >>> loss = criterion(torch.randn(2, 4, requires_grad=True), torch.randn(2, 4))
    >>> loss
    tensor(..., grad_fn=<SmoothL1LossBackward0>)
    >>> loss.backward()

    ```
    """

    def __init__(
        self,
        criterion: nn.Module | dict,
        prediction: nn.Module | dict | None = None,
        target: nn.Module | dict | None = None,
    ) -> None:
        super().__init__()
        self.criterion = setup_module(criterion)
        self.prediction = setup_module(prediction or nn.Identity())
        self.target = setup_module(target or nn.Identity())

    def forward(self, prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        prediction = self.prediction(prediction)
        target = self.target(target)
        return self.criterion(prediction, target)
