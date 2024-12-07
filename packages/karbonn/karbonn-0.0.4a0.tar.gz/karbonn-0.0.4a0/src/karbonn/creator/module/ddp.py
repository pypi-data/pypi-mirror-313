r"""Contain a module creator that returns a ``DistributedDataParallel``
module."""

from __future__ import annotations

__all__ = ["to_ddp"]

import logging
from typing import TYPE_CHECKING

from torch.distributed import Backend
from torch.nn.parallel import DistributedDataParallel

from karbonn.utils.imports import check_ignite, is_ignite_available

if is_ignite_available():  # pragma: no cover
    from ignite import distributed as idist

if TYPE_CHECKING:
    from torch import nn

logger = logging.getLogger(__name__)


def to_ddp(module: nn.Module, ddp_kwargs: dict | None = None) -> nn.Module:
    r"""Wrap a module with the ``DistributedDataParallel`` module.

    Args:
        module: The module to wrap with ``DistributedDataParallel``.
            The module should be compatible with
            ``DistributedDataParallel``. If you use NCCL, the module
            should be on a CUDA device.
        ddp_kwargs: Some keyword arguments used to instantiate the
            ``DistributedDataParallel``. Please read the documentation
            of ``DistributedDataParallel`` to see the possible options.
            Note that it is not possible to set ``module`` and
            ``device_ids`` with a keyword argument.

    Returns:
        The input module wrapped in a ``DistributedDataParallel``
            module.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.creator.module.ddp import to_ddp
    >>> to_ddp(torch.nn.Linear(4, 6))

    ```
    """
    if isinstance(module, DistributedDataParallel):
        logger.warning(
            "No operation is performed because the module is already a 'DistributedDataParallel'"
        )
        return module
    ddp_kwargs = ddp_kwargs or {}
    check_ignite()
    backend = idist.backend()
    if backend == Backend.NCCL:
        lrank = idist.get_local_rank()
        logger.info(f"Applying 'DistributedDataParallel' on module, device id: {lrank}")
        return DistributedDataParallel(module, device_ids=[lrank], **ddp_kwargs)
    if backend == Backend.GLOO:
        logger.info("Applying 'DistributedDataParallel' on module")
        return DistributedDataParallel(module, **ddp_kwargs)
    return module
