r"""Define some PyTest fixtures."""

from __future__ import annotations

__all__ = [
    "cuda_available",
    "distributed_available",
    "gloo_available",
    "ignite_available",
    "nccl_available",
    "objectory_available",
    "sklearn_available",
    "tabulate_available",
    "two_gpus_available",
]

import pytest
import torch

from karbonn.utils.imports import (
    is_ignite_available,
    is_objectory_available,
    is_sklearn_available,
    is_tabulate_available,
)

cuda_available = pytest.mark.skipif(
    not torch.cuda.is_available(), reason="Requires a device with CUDA"
)
two_gpus_available = pytest.mark.skipif(
    torch.cuda.device_count() < 2, reason="Requires at least 2 GPUs"
)
distributed_available = pytest.mark.skipif(
    not torch.distributed.is_available(), reason="Requires PyTorch distributed"
)
gloo_available = pytest.mark.skipif(
    not torch.distributed.is_gloo_available(),
    reason="Requires PyTorch distributed and GLOO backend",
)
nccl_available = pytest.mark.skipif(
    not torch.distributed.is_nccl_available(),
    reason="Requires PyTorch distributed and NCCL backend",
)

ignite_available = pytest.mark.skipif(not is_ignite_available(), reason="Require pytorch-ignite")
objectory_available = pytest.mark.skipif(not is_objectory_available(), reason="Require objectory")
sklearn_available = pytest.mark.skipif(not is_sklearn_available(), reason="Require sklearn")
tabulate_available = pytest.mark.skipif(not is_tabulate_available(), reason="Require tabulate")
