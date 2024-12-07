r"""Contain formatting utility functions."""

from __future__ import annotations

__all__ = ["str_table"]

from typing import Any

from karbonn.utils.imports import is_tabulate_available

if is_tabulate_available():  # pragma: no cover
    from tabulate import tabulate


def str_table(data: Any, **kwargs: Any) -> str:
    r"""Return a string representation of tabular data.

    Internally, this function uses ``tabulate`` package to compute the
    string representation of tabular data. If ``tabulate``, it just
    uses the ``str`` function.

    Args:
        data: The tabular data to convert.
        **kwargs: The keyword arguments to pass to
            ``tabulate.tabulate`` function.

    Returns:
        The string representation of tabular data

    ```pycon

    >>> from karbonn.utils.format import str_table
    >>> data = [
    ...     ["col1", "col2", "col3"],
    ...     [10, 20, 30],
    ...     [11, 21, 31],
    ...     [12, 22, 32],
    ...     [13, 23, 33],
    ... ]
    >>> print(str_table(data, tablefmt="heavy_grid"))
    ┏━━━━━━┳━━━━━━┳━━━━━━┓
    ┃ col1 ┃ col2 ┃ col3 ┃
    ┣━━━━━━╋━━━━━━╋━━━━━━┫
    ┃ 10   ┃ 20   ┃ 30   ┃
    ┣━━━━━━╋━━━━━━╋━━━━━━┫
    ┃ 11   ┃ 21   ┃ 31   ┃
    ┣━━━━━━╋━━━━━━╋━━━━━━┫
    ┃ 12   ┃ 22   ┃ 32   ┃
    ┣━━━━━━╋━━━━━━╋━━━━━━┫
    ┃ 13   ┃ 23   ┃ 33   ┃
    ┗━━━━━━┻━━━━━━┻━━━━━━┛

    ```
    """
    if is_tabulate_available():
        return tabulate(data, **kwargs)
    return str(data)
