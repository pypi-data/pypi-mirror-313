r"""Contain functionalities to analyze a ``torch.nn.Module``."""

from __future__ import annotations

__all__ = [
    "ModuleSummary",
    "get_in_dtype",
    "get_in_size",
    "get_layer_names",
    "get_layer_types",
    "get_num_learnable_parameters",
    "get_num_parameters",
    "get_out_dtype",
    "get_out_size",
    "merge_size_dtype",
    "module_summary",
    "multiline_format",
    "parse_batch_dtype",
    "parse_batch_shape",
    "str_module_summary",
]

from collections.abc import Mapping, Sequence
from itertools import starmap
from typing import TYPE_CHECKING, Any, overload

import torch
from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from torch import nn

from karbonn.utils.format import str_table
from karbonn.utils.iterator import get_named_modules
from karbonn.utils.params import num_learnable_parameters, num_parameters

if TYPE_CHECKING:
    from torch.utils.hooks import RemovableHandle

PARAMETER_NUM_UNITS = (" ", "K", "M", "B", "T")
UNKNOWN_SIZE = "?"
UNKNOWN_DTYPE = "?"


class ModuleSummary:
    r"""Summary class for a single layer in a ``torch.nn.Module``.

    It collects the following information:

    - Type of the layer (e.g. Linear, BatchNorm1d, ...)
    - Input shape
    - Output shape
    - Input data type
    - Output data type
    - Number of parameters
    - Number of learnable parameters

    The input and output shapes are only known after the example input
    array was passed through the model.

    Args:
        module: A module to summarize.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary import ModuleSummary
    >>> module = torch.nn.Conv2d(3, 8, 3)
    >>> summary = ModuleSummary(module)
    >>> summary.get_num_parameters()
    224
    >>> summary.get_num_learnable_parameters()
    224
    >>> summary.get_layer_type()
    'Conv2d'
    >>> output = module(torch.rand(1, 3, 5, 5))
    >>> summary.get_in_size()
    torch.Size([1, 3, 5, 5])
    >>> summary.get_out_size()
    torch.Size([1, 8, 3, 3])
    >>> summary.get_in_dtype()
    torch.float32
    >>> summary.get_out_dtype()
    torch.float32
    >>> summary
    ModuleSummary(
      (module): Conv2d(3, 8, kernel_size=(3, 3), stride=(1, 1))
      (in_size): torch.Size([1, 3, 5, 5])
      (out_size): torch.Size([1, 8, 3, 3])
      (in_dtype): torch.float32
      (out_dtype): torch.float32
    )

    ```
    """

    def __init__(self, module: nn.Module) -> None:
        super().__init__()
        self.module = module
        self._hook_handle = self._register_hook()
        self._in_size = None
        self._out_size = None
        self._in_dtype = None
        self._out_dtype = None

    def __del__(self) -> None:
        self.detach_hook()

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "module": self.module,
                    "in_size": self._in_size,
                    "out_size": self._out_size,
                    "in_dtype": self._in_dtype,
                    "out_dtype": self._out_dtype,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "module": self.module,
                    "in_size": self._in_size,
                    "out_size": self._out_size,
                    "in_dtype": self._in_dtype,
                    "out_dtype": self._out_dtype,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def _register_hook(self) -> RemovableHandle:
        r"""Register a hook on the module that computes the input and
        output size(s) on the first forward pass.

        If the hook is called, it will remove itself from the module,
        meaning that recursive models will only record their input and
        output shapes once.

        Return:
            A handle for the installed hook.
        """

        def hook(module: nn.Module, inp: Any, out: Any) -> None:  # noqa: ARG001
            if len(inp) == 1:
                inp = inp[0]
            self._in_size = parse_batch_shape(inp)
            self._out_size = parse_batch_shape(out)
            self._in_dtype = parse_batch_dtype(inp)
            self._out_dtype = parse_batch_dtype(out)
            self._hook_handle.remove()

        return self.module.register_forward_hook(hook)

    def detach_hook(self) -> None:
        r"""Remove the forward hook if it was not already removed in the
        forward pass.

        Will be called after the summary is created.
        """
        self._hook_handle.remove()

    def get_in_dtype(
        self,
    ) -> tuple[torch.dtype | None, ...] | dict[str, torch.dtype | None] | torch.dtype | None:
        r"""Return the input tensors data type.

        Returns:
            The input tensors data type.
        """
        return self._in_dtype

    def get_out_dtype(
        self,
    ) -> tuple[torch.dtype | None, ...] | dict[str, torch.dtype | None] | torch.dtype | None:
        r"""Return the output tensors data type.

        Returns:
            The output tensors data type.
        """
        return self._out_dtype

    def get_in_size(
        self,
    ) -> tuple[torch.Size | None, ...] | dict[str, torch.Size | None] | torch.Size | None:
        r"""Return the input tensors shapes.

        Returns:
            The input tensors shapes.
        """
        return self._in_size

    def get_out_size(
        self,
    ) -> tuple[torch.Size | None, ...] | dict[str, torch.Size | None] | torch.Size | None:
        r"""Return the output tensors shapes.

        Returns:
            The output tensors shapes.
        """
        return self._out_size

    def get_layer_type(self) -> str:
        r"""Return the class name of the module.

        Returns:
            The class name of the module.
        """
        return str(self.module.__class__.__qualname__)

    def get_num_parameters(self) -> int:
        r"""Return the number of parameters in this module.

        Returns:
            The number of parameters.
        """
        return num_parameters(self.module)

    def get_num_learnable_parameters(self) -> int:
        r"""Return the number of learnable parameters in this module.

        Returns:
            The number of learnable parameters.
        """
        return num_learnable_parameters(self.module)


@overload
def parse_batch_dtype(batch: torch.Tensor) -> torch.dtype | None: ...  # pragma: no cover


@overload
def parse_batch_dtype(
    batch: Sequence[torch.Tensor],
) -> tuple[torch.dtype | None, ...]: ...  # pragma: no cover


@overload
def parse_batch_dtype(
    batch: Mapping[str, torch.Tensor]
) -> dict[str, torch.dtype | None]: ...  # pragma: no cover


def parse_batch_dtype(
    batch: Any,
) -> tuple[torch.dtype | None, ...] | dict[str, torch.dtype | None] | torch.dtype | None:
    r"""Parse the data type of the tensors in the batch.

    The current implementation only parses the data type of a tensor,
    list of tensors, and dictionary of tensors.

    Args:
        batch: The batch to parse.

    Returns:
        The data types in the batch or ``None`` if it cannot parse the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary.module import parse_batch_dtype
    >>> parse_batch_dtype(torch.ones(2, 3))
    torch.float32
    >>> parse_batch_dtype([torch.ones(2, 3), torch.zeros(2, dtype=torch.long)])
    (torch.float32, torch.int64)
    >>> parse_batch_dtype(
    ...     {"input1": torch.ones(2, 3), "input2": torch.zeros(2, dtype=torch.long)}
    ... )
    {'input1': torch.float32, 'input2': torch.int64}

    ```
    """
    if torch.is_tensor(batch):
        return batch.dtype
    if isinstance(batch, Sequence):
        return tuple(parse_batch_dtype(item) for item in batch)
    if isinstance(batch, Mapping):
        return {key: parse_batch_dtype(value) for key, value in batch.items()}
    return None


@overload
def parse_batch_shape(batch: torch.Tensor) -> torch.Size | None: ...  # pragma: no cover


@overload
def parse_batch_shape(
    batch: Sequence[torch.Tensor],
) -> tuple[torch.Size | None, ...]: ...  # pragma: no cover


@overload
def parse_batch_shape(
    batch: Mapping[str, torch.Tensor]
) -> dict[str, torch.Size | None]: ...  # pragma: no cover


def parse_batch_shape(
    batch: Any,
) -> tuple[torch.Size | None, ...] | dict[str, torch.Size | None] | torch.Size | None:
    r"""Parse the shapes of the tensors in the batch.

    The current implementation only parses the shapes of  tensor,
    list of tensors, and dictionary of tensors.

    Args:
        batch: The batch to parse.

    Returns:
        The shapes in the batch or ``None`` if it cannot parse the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary.module import parse_batch_shape
    >>> parse_batch_shape(torch.ones(2, 3))
    torch.Size([2, 3])
    >>> parse_batch_shape([torch.ones(2, 3), torch.zeros(2)])
    (torch.Size([2, 3]), torch.Size([2]))
    >>> parse_batch_shape({"input1": torch.ones(2, 3), "input2": torch.zeros(2)})
    {'input1': torch.Size([2, 3]), 'input2': torch.Size([2])}

    ```
    """
    if torch.is_tensor(batch):
        return batch.shape
    if isinstance(batch, Sequence):
        return tuple(parse_batch_shape(item) for item in batch)
    if isinstance(batch, Mapping):
        return {key: parse_batch_shape(value) for key, value in batch.items()}
    return None


def module_summary(
    module: nn.Module, depth: int = 0, input_args: Any = None, input_kwargs: Any = None
) -> dict[str, ModuleSummary]:
    r"""Return the per module summary.

    Args:
        module: The module to summarize.
        depth: The maximum depth of the module to summarize.
        input_args: Positional arguments that are passed to the module
            to  compute the shapes and data types of the inputs and
            outputs of each module.
        input_kwargs: Keyword arguments that are passed to the module
            to  compute the shapes and data types of the inputs and
            outputs of each module.

    Returns:
        The summary of each module.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary import module_summary
    >>> module = torch.nn.Sequential(
    ...     torch.nn.Linear(4, 6), torch.nn.ReLU(), torch.nn.Linear(6, 3)
    ... )
    >>> summary = module_summary(module, depth=1)
    >>> summary
    {'[root]': ModuleSummary(
      (module): Sequential(
          (0): Linear(in_features=4, out_features=6, bias=True)
          (1): ReLU()
          (2): Linear(in_features=6, out_features=3, bias=True)
        )
      (in_size): None
      (out_size): None
      (in_dtype): None
      (out_dtype): None
    ),
    '0': ModuleSummary(
      (module): Linear(in_features=4, out_features=6, bias=True)
      (in_size): None
      (out_size): None
      (in_dtype): None
      (out_dtype): None
    ),
    '1': ModuleSummary(
      (module): ReLU()
      (in_size): None
      (out_size): None
      (in_dtype): None
      (out_dtype): None
    ),
    '2': ModuleSummary(
      (module): Linear(in_features=6, out_features=3, bias=True)
      (in_size): None
      (out_size): None
      (in_dtype): None
      (out_dtype): None
    )}
    >>> summary = module_summary(module, depth=1, input_args=[torch.randn(2, 4)])
    >>> summary
    {'[root]': ModuleSummary(
      (module): Sequential(
          (0): Linear(in_features=4, out_features=6, bias=True)
          (1): ReLU()
          (2): Linear(in_features=6, out_features=3, bias=True)
        )
      (in_size): torch.Size([2, 4])
      (out_size): torch.Size([2, 3])
      (in_dtype): torch.float32
      (out_dtype): torch.float32
    ),
    '0': ModuleSummary(
      (module): Linear(in_features=4, out_features=6, bias=True)
      (in_size): torch.Size([2, 4])
      (out_size): torch.Size([2, 6])
      (in_dtype): torch.float32
      (out_dtype): torch.float32
    ),
    '1': ModuleSummary(
      (module): ReLU()
      (in_size): torch.Size([2, 6])
      (out_size): torch.Size([2, 6])
      (in_dtype): torch.float32
      (out_dtype): torch.float32
    ),
    '2': ModuleSummary(
      (module): Linear(in_features=6, out_features=3, bias=True)
      (in_size): torch.Size([2, 6])
      (out_size): torch.Size([2, 3])
      (in_dtype): torch.float32
      (out_dtype): torch.float32
    )}

    ```
    """
    summary = {name: ModuleSummary(layer) for name, layer in get_named_modules(module, depth=depth)}
    if input_args is not None or input_kwargs is not None:
        module(*(input_args or []), **(input_kwargs or {}))
    for layer in summary.values():
        layer.detach_hook()
    return summary


def str_module_summary(summary: dict[str, ModuleSummary], tablefmt: str = "fancy_grid") -> str:
    r"""Return a string containing a tabular representation of the
    summary.

    This function uses ``tabulate`` to generate the table if it is
    available.

    Args:
        summary: The summary of each layer.
        tablefmt: The table format. You can find the valid formats at
            https://pypi.org/project/tabulate/.

    Returns:
        A string containing a tabular representation of the summary.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary import module_summary, str_module_summary
    >>> module = torch.nn.Sequential(
    ...     torch.nn.Linear(4, 6), torch.nn.ReLU(), torch.nn.Linear(6, 3)
    ... )
    >>> summary = module_summary(module, depth=1, input_args=[torch.randn(2, 4)])
    >>> print(str_module_summary(summary))
    ╒════╤════════╤════════════╤══════════════════╤════════════════════════╤════════════════════════╕
    │    │ name   │ type       │ params (learn)   │ in size (dtype)        │ out size (dtype)       │
    ╞════╪════════╪════════════╪══════════════════╪════════════════════════╪════════════════════════╡
    │  0 │ [root] │ Sequential │ 51 (51)          │ [2, 4] (torch.float32) │ [2, 3] (torch.float32) │
    ├────┼────────┼────────────┼──────────────────┼────────────────────────┼────────────────────────┤
    │  1 │ 0      │ Linear     │ 30 (30)          │ [2, 4] (torch.float32) │ [2, 6] (torch.float32) │
    ├────┼────────┼────────────┼──────────────────┼────────────────────────┼────────────────────────┤
    │  2 │ 1      │ ReLU       │ 0 (0)            │ [2, 6] (torch.float32) │ [2, 6] (torch.float32) │
    ├────┼────────┼────────────┼──────────────────┼────────────────────────┼────────────────────────┤
    │  3 │ 2      │ Linear     │ 21 (21)          │ [2, 6] (torch.float32) │ [2, 3] (torch.float32) │
    ╘════╧════════╧════════════╧══════════════════╧════════════════════════╧════════════════════════╛

    ```
    """
    tab = {
        "name": get_layer_names(summary),
        "type": get_layer_types(summary),
        "params (learn)": [
            f"{params:,} ({lparams:,})"
            for params, lparams in zip(
                get_num_parameters(summary), get_num_learnable_parameters(summary)
            )
        ],
        "in size (dtype)": merge_size_dtype(
            sizes=get_in_size(summary), dtypes=get_in_dtype(summary)
        ),
        "out size (dtype)": merge_size_dtype(
            sizes=get_out_size(summary), dtypes=get_out_dtype(summary)
        ),
    }
    return str_table(tab, headers="keys", tablefmt=tablefmt, showindex="always")


def multiline_format(rows: Sequence[str | Sequence[str] | Mapping[str, str]]) -> list[str]:
    r"""Return a sequence of formatted rows.

    Args:
        rows: The raw rows.

    Returns:
        The formatted rows.
    """
    formatted_rows = []
    for row in rows:
        if isinstance(row, str):
            formatted_rows.append(row)
        elif isinstance(row, Sequence):
            formatted_rows.append("\n".join([f"({i}): {r}" for i, r in enumerate(row)]))
        elif isinstance(row, Mapping):
            formatted_rows.append("\n".join([f"({key}): {value}" for key, value in row.items()]))
    return formatted_rows


def get_layer_names(summary: dict[str, ModuleSummary]) -> list[str]:
    r"""Get the name of each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The layer names.
    """
    return list(summary.keys())


def get_layer_types(summary: dict[str, ModuleSummary]) -> list[str]:
    r"""Get the class name of each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The class names.
    """
    return [layer.get_layer_type() for layer in summary.values()]


def get_num_parameters(summary: dict[str, ModuleSummary]) -> list[int]:
    r"""Return the number of parameters for each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The number of parameters.
    """
    return [layer.get_num_parameters() for layer in summary.values()]


def get_num_learnable_parameters(summary: dict[str, ModuleSummary]) -> list[int]:
    r"""Return the number of learnable parameters for each layer in the
    summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The number of learnable parameters.
    """
    return [layer.get_num_learnable_parameters() for layer in summary.values()]


def get_in_dtype(
    summary: dict[str, ModuleSummary]
) -> list[torch.dtype | Sequence[torch.dtype] | Mapping[str, torch.dtype]]:
    r"""Return the input tensors data type for each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The input tensors data types.
    """
    return [layer.get_in_dtype() for layer in summary.values()]


def get_out_dtype(
    summary: dict[str, ModuleSummary]
) -> list[torch.dtype | Sequence[torch.dtype] | Mapping[str, torch.dtype]]:
    r"""Return the output tensors data type for each layer in the
    summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The output tensors data types.
    """
    return [layer.get_out_dtype() for layer in summary.values()]


def get_in_size(
    summary: dict[str, ModuleSummary]
) -> list[torch.Size | Sequence[torch.Size] | Mapping[str, torch.Size]]:
    r"""Return the input tensors shapes for each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The input tensors shapes.
    """
    return [layer.get_in_size() for layer in summary.values()]


def get_out_size(
    summary: dict[str, ModuleSummary]
) -> list[torch.Size | Sequence[torch.Size] | Mapping[str, torch.Size]]:
    r"""Return the output tensors shapes for each layer in the summary.

    Args:
        summary: The summary of each layer.

    Returns:
        The output tensors shapess.
    """
    return [layer.get_out_size() for layer in summary.values()]


def merge_size_dtype(
    sizes: list[torch.Size | Sequence[torch.Size] | Mapping[str, torch.Size]],
    dtypes: list[torch.dtype | Sequence[torch.dtype] | Mapping[str, torch.dtype]],
) -> list[str]:
    r"""Return joined string representations of the sizes and data types.

    Args:
        sizes: The sizes to join. It must have the same structure
            as ``dtypes``.
        dtypes: The data types to join. It must have the same
            structure as ``sizes``.

    Returns:
        The joined string representations.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.summary.module import merge_size_dtype
    >>> out = merge_size_dtype(
    ...     sizes=[
    ...         torch.Size([2, 3]),
    ...         [torch.Size([2, 4]), torch.Size([2, 5]), torch.Size([2, 6, 3])],
    ...         {"input1": torch.Size([2, 4]), "input2": torch.Size([2, 3, 4])},
    ...     ],
    ...     dtypes=[
    ...         torch.float32,
    ...         [torch.float32, torch.long, torch.float],
    ...         {"input1": torch.long, "input2": torch.float32},
    ...     ],
    ... )
    >>> out
    ['[2, 3] (torch.float32)',
     '(0): [2, 4] (torch.float32)\n(1): [2, 5] (torch.int64)\n(2): [2, 6, 3] (torch.float32)',
     '(input1): [2, 4] (torch.int64)\n(input2): [2, 3, 4] (torch.float32)']

    ```
    """

    def to_str(size: torch.Size, dtype: torch.dtype) -> str:
        return f"{list(size)} ({dtype})"

    output = []
    for size, dtype in zip(sizes, dtypes):
        if isinstance(dtype, torch.dtype):
            output.append(to_str(size, dtype))
        elif isinstance(dtype, Sequence):
            output.append(list(starmap(to_str, zip(size, dtype))))
        elif isinstance(dtype, Mapping):
            output.append({k: to_str(s, dtype[k]) for k, s in size.items()})
        else:
            output.append("? (?)")
    return multiline_format(output)
