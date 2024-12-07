r"""Contain utility functions."""

from __future__ import annotations

__all__ = [
    "create_sequential",
    "find_module_state_dict",
    "freeze_module",
    "get_module_device",
    "get_module_devices",
    "has_learnable_parameters",
    "has_parameters",
    "is_loss_decreasing",
    "is_loss_decreasing_with_adam",
    "is_loss_decreasing_with_sgd",
    "is_module_config",
    "is_module_on_device",
    "load_state_dict_to_module",
    "module_mode",
    "num_learnable_parameters",
    "num_parameters",
    "setup_module",
    "top_module_mode",
    "unfreeze_module",
]

from karbonn.utils.device import (
    get_module_device,
    get_module_devices,
    is_module_on_device,
)
from karbonn.utils.factory import create_sequential, is_module_config, setup_module
from karbonn.utils.loss import (
    is_loss_decreasing,
    is_loss_decreasing_with_adam,
    is_loss_decreasing_with_sgd,
)
from karbonn.utils.mode import module_mode, top_module_mode
from karbonn.utils.params import (
    freeze_module,
    has_learnable_parameters,
    has_parameters,
    num_learnable_parameters,
    num_parameters,
    unfreeze_module,
)
from karbonn.utils.state_dict import find_module_state_dict, load_state_dict_to_module
