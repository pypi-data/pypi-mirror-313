r"""Contain some functionalities to analyze the parameters of a
``torch.nn.Module``."""

from __future__ import annotations

__all__ = [
    "NO_PARAMETER",
    "PARAMETER_NOT_INITIALIZED",
    "ParameterSummary",
    "get_parameter_summaries",
    "str_parameter_summary",
]

import logging
from dataclasses import asdict, dataclass
from itertools import starmap
from typing import TYPE_CHECKING, Any

from coola.nested import convert_to_dict_of_lists
from torch.nn import Module, Parameter, UninitializedParameter

from karbonn.utils.format import str_table

if TYPE_CHECKING:
    import torch


logger = logging.getLogger(__name__)

PARAMETER_NOT_INITIALIZED = "NI"
NO_PARAMETER = "NP"


@dataclass
class ParameterSummary:
    r"""Implement a class to easily manage a parameter summary.

    NI: Not Initialized
    NP: No Parameter
    """

    name: str
    mean: float | str
    median: float | str
    std: float | str
    min: float | str
    max: float | str
    shape: tuple[int, ...] | str
    learnable: bool | str
    device: torch.device | str

    @classmethod
    def from_parameter(
        cls, name: str, parameter: Parameter | UninitializedParameter
    ) -> ParameterSummary:
        r"""Create the parameter summary from the parameter object.

        Args:
            name: The name of the parameter.
            parameter: The parameter object.

        Returns:
            The parameter summary.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.utils.summary import ParameterSummary
        >>> ParameterSummary.from_parameter("weight", torch.nn.Parameter(torch.ones(6, 4)))
        ParameterSummary(name='weight', mean=1.0, median=1.0, std=0.0, min=1.0, max=1.0, shape=(6, 4), learnable=True, device=device(type='cpu'))

        ```
        """
        if isinstance(parameter, UninitializedParameter):
            return cls(
                name=name,
                mean=PARAMETER_NOT_INITIALIZED,
                median=PARAMETER_NOT_INITIALIZED,
                std=PARAMETER_NOT_INITIALIZED,
                min=PARAMETER_NOT_INITIALIZED,
                max=PARAMETER_NOT_INITIALIZED,
                shape=PARAMETER_NOT_INITIALIZED,
                learnable=parameter.requires_grad,
                device=parameter.device,
            )
        if parameter.numel() == 0:
            return cls(
                name=name,
                mean=NO_PARAMETER,
                median=NO_PARAMETER,
                std=NO_PARAMETER,
                min=NO_PARAMETER,
                max=NO_PARAMETER,
                shape=tuple(parameter.shape),
                learnable=parameter.requires_grad,
                device=parameter.device,
            )
        return cls(
            name=name,
            mean=parameter.mean().item(),
            median=parameter.median().item(),
            std=parameter.std().item(),
            min=parameter.min().item(),
            max=parameter.max().item(),
            shape=tuple(parameter.shape),
            learnable=parameter.requires_grad,
            device=parameter.device,
        )


def get_parameter_summaries(module: Module) -> list[ParameterSummary]:
    r"""Return the parameter summaries of a module.

    Args:
        module: The module with the parameters to summarize.

    Returns:
        The list of parameter summaries.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary import get_parameter_summaries
    >>> get_parameter_summaries(torch.nn.Linear(4, 6))
    [ParameterSummary(name='weight', mean=..., median=..., std=..., min=..., max=..., shape=(6, 4), learnable=True, device=device(type='cpu')),
     ParameterSummary(name='bias', mean=..., median=..., std=..., min=..., max=..., shape=(6,), learnable=True, device=device(type='cpu'))]

    ```
    """
    return list(starmap(ParameterSummary.from_parameter, module.named_parameters()))


def str_parameter_summary(
    module: Module, tablefmt: str = "fancy_outline", floatfmt: str = ".6f", **kwargs: Any
) -> str:
    r"""Return a string summary of the model parameters.

    This function uses ``tabulate`` to generate the table if it is
    available.

    Args:
        module: The module to analyze.
        tablefmt: The table format.
        floatfmt: The float format.
        kwargs: Variable keyword arguments to pass to ``tabulate``.

    Returns:
        The string summary of the model parameters

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary import str_parameter_summary
    >>> linear = torch.nn.Linear(4, 6)
    >>> torch.nn.init.ones_(linear.weight)
    >>> torch.nn.init.zeros_(linear.bias)
    >>> desc = str_parameter_summary(linear)
    >>> print(desc)
    ╒════════╤══════════╤══════════╤══════════╤══════════╤══════════╤═════════╤═════════════╤══════════╕
    │ name   │     mean │   median │      std │      min │      max │ shape   │ learnable   │ device   │
    ╞════════╪══════════╪══════════╪══════════╪══════════╪══════════╪═════════╪═════════════╪══════════╡
    │ weight │ 1.000000 │ 1.000000 │ 0.000000 │ 1.000000 │ 1.000000 │ (6, 4)  │ True        │ cpu      │
    │ bias   │ 0.000000 │ 0.000000 │ 0.000000 │ 0.000000 │ 0.000000 │ (6,)    │ True        │ cpu      │
    ╘════════╧══════════╧══════════╧══════════╧══════════╧══════════╧═════════╧═════════════╧══════════╛

    ```
    """
    summaries = convert_to_dict_of_lists(
        [asdict(summary) for summary in get_parameter_summaries(module)]
    )
    return str_table(summaries, headers="keys", tablefmt=tablefmt, floatfmt=floatfmt, **kwargs)
