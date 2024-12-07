r"""Contain utility functions to check if the loss is decreasing."""

from __future__ import annotations

__all__ = ["is_loss_decreasing", "is_loss_decreasing_with_adam", "is_loss_decreasing_with_sgd"]


import logging
from typing import TYPE_CHECKING

from coola.random import torch_seed
from torch.nn.utils import clip_grad_norm_
from torch.optim import SGD, Adam, Optimizer

from karbonn.utils.mode import module_mode

if TYPE_CHECKING:
    from collections.abc import Callable

    from torch import Tensor
    from torch.nn import Module

logger = logging.getLogger(__name__)


def is_loss_decreasing(
    module: Module,
    criterion: Module | Callable[[Tensor, Tensor], Tensor],
    optimizer: Optimizer,
    feature: Tensor,
    target: Tensor,
    num_iterations: int = 1,
    random_seed: int = 10772155803920552556,
) -> bool:
    r"""Check if the loss decreased after some iterations.

    Args:
        module: The module to test. The module must have a single
            input tensor and a single output tensor.
        criterion: The criterion to test.
        optimizer: The optimizer to update the weights of the model.
        feature: The input of the module.
        target: The target used to compute the loss.
        num_iterations: The number of optimization steps.
        random_seed: The random seed to make the function
            deterministic if the module contains randomness.

    Returns:
        ``True`` if the loss decreased after some iterations,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from torch import nn
    >>> from karbonn.utils import is_loss_decreasing
    >>> module = nn.Linear(4, 2)
    >>> is_loss_decreasing(
    ...     module=module,
    ...     criterion=nn.MSELoss(),
    ...     optimizer=SGD(module.parameters(), lr=0.01),
    ...     feature=torch.rand(4, 4),
    ...     target=torch.rand(4, 2),
    ... )
    True

    ```
    """
    with module_mode(module):
        module.eval()
        with torch_seed(random_seed):
            initial_loss = criterion(module(feature), target).item()
        logger.debug(f"Initial loss value: {initial_loss}")

        module.train()
        for _ in range(num_iterations):
            optimizer.zero_grad()
            loss = criterion(module(feature), target)
            loss.backward()
            clip_grad_norm_(module.parameters(), max_norm=1, norm_type=2)
            optimizer.step()

        module.eval()
        with torch_seed(random_seed):
            final_loss = criterion(module(feature), target).item()
        logger.debug(f"Final loss value: {final_loss}")
    return final_loss < initial_loss


def is_loss_decreasing_with_adam(
    module: Module,
    criterion: Module | Callable[[Tensor, Tensor], Tensor],
    feature: Tensor,
    target: Tensor,
    lr: float = 0.0003,
    num_iterations: int = 1,
    random_seed: int = 10772155803920552556,
) -> bool:
    r"""Check if the loss decreased after some iterations.

    The module is trained with the Adam optimizer.

    Args:
        module: The module to test. The module must have a single
            input tensor and a single output tensor.
        criterion: The criterion to test.
        feature: The input of the module.
        target: The target used to compute the loss.
        lr: The learning rate.
        num_iterations: The number of optimization steps.
        random_seed: The random seed to make the function
            deterministic if the module contains randomness.

    Returns:
        ``True`` if the loss decreased after some iterations,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from torch import nn
    >>> from karbonn.utils import is_loss_decreasing_with_adam
    >>> is_loss_decreasing_with_adam(
    ...     module=nn.Linear(4, 2),
    ...     criterion=nn.MSELoss(),
    ...     feature=torch.rand(4, 4),
    ...     target=torch.rand(4, 2),
    ...     lr=0.0003,
    ... )
    True

    ```
    """
    return is_loss_decreasing(
        module=module,
        criterion=criterion,
        optimizer=Adam(module.parameters(), lr=lr),
        feature=feature,
        target=target,
        num_iterations=num_iterations,
        random_seed=random_seed,
    )


def is_loss_decreasing_with_sgd(
    module: Module,
    criterion: Module | Callable[[Tensor, Tensor], Tensor],
    feature: Tensor,
    target: Tensor,
    lr: float = 0.01,
    num_iterations: int = 1,
    random_seed: int = 10772155803920552556,
) -> bool:
    r"""Check if the loss decreased after some iterations.

    The module is trained with the ``torch.optim.SGD`` optimizer.

    Args:
        module: The module to test. The module must have a single
            input tensor and a single output tensor.
        criterion: The criterion to test.
        feature: The input of the module.
        target: The target used to compute the loss.
        num_iterations: The number of optimization steps.
        lr: The learning rate.
        random_seed: The random seed to make the function
            deterministic if the module contains randomness.

    Returns:
        ``True`` if the loss decreased after some iterations,
            otherwise ``False``.

    Example usage:

    ```pycon

    >>> import torch
    >>> from torch import nn
    >>> from karbonn.utils import is_loss_decreasing_with_adam
    >>> is_loss_decreasing_with_adam(
    ...     module=nn.Linear(4, 2),
    ...     criterion=nn.MSELoss(),
    ...     feature=torch.rand(4, 4),
    ...     target=torch.rand(4, 2),
    ...     lr=0.01,
    ... )
    True

    ```
    """
    return is_loss_decreasing(
        module=module,
        criterion=criterion,
        optimizer=SGD(module.parameters(), lr=lr),
        feature=feature,
        target=target,
        num_iterations=num_iterations,
        random_seed=random_seed,
    )
