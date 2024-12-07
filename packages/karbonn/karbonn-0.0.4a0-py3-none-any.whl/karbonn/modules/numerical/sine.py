r"""Contain modules to encode numerical values using cosine and sine
functions."""

from __future__ import annotations

__all__ = [
    "AsinhCosSinNumericalEncoder",
    "CosSinNumericalEncoder",
    "check_abs_range",
    "check_frequency",
    "prepare_tensor_param",
]

import math
from typing import TYPE_CHECKING

import torch
from torch.nn import Module, Parameter

if TYPE_CHECKING:
    from torch import Tensor


class CosSinNumericalEncoder(Module):
    r"""Implement a frequency/phase-shift numerical encoder where the
    periodic functions are cosine and sine.

    Args:
        frequency: The initial frequency values. This input should be
            a tensor of shape ``(n_features, feature_size // 2)`` or
            ``(feature_size // 2,)``.
        phase_shift: The initial phase-shift values. This input should
            be a tensor of shape ``(n_features, feature_size // 2)`` or
            ``(feature_size // 2,)``.
        learnable: If ``True`` the frequencies and phase-shift
            parameters are learnable, otherwise they are frozen.

    Shape:
        - Input: ``(*, n_features)``, where ``*`` means any number of
            dimensions.
        - Output: ``(*, n_features, feature_size)``,  where ``*`` has
            the same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import CosSinNumericalEncoder
    >>> # Example with 1 feature
    >>> m = CosSinNumericalEncoder(
    ...     frequency=torch.tensor([[1.0, 2.0, 4.0]]),
    ...     phase_shift=torch.zeros(1, 3),
    ... )
    >>> m
    CosSinNumericalEncoder(frequency=(1, 6), phase_shift=(1, 6), learnable=False)
    >>> out = m(torch.tensor([[0.0], [1.0], [2.0], [3.0]]))
    >>> out
    tensor([[[ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000]],
            [[ 0.8415,  0.9093, -0.7568,  0.5403, -0.4161, -0.6536]],
            [[ 0.9093, -0.7568,  0.9894, -0.4161, -0.6536, -0.1455]],
            [[ 0.1411, -0.2794, -0.5366, -0.9900,  0.9602,  0.8439]]])
    >>> # Example with 2 features
    >>> m = CosSinNumericalEncoder(
    ...     frequency=torch.tensor([[1.0, 2.0, 4.0], [2.0, 4.0, 6.0]]),
    ...     phase_shift=torch.zeros(2, 3),
    ... )
    >>> m
    CosSinNumericalEncoder(frequency=(2, 6), phase_shift=(2, 6), learnable=False)
    >>> out = m(torch.tensor([[0.0, 3.0], [1.0, 2.0], [2.0, 1.0], [3.0, 0.0]]))
    >>> out
    tensor([[[ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000],
             [-0.2794, -0.5366, -0.7510,  0.9602,  0.8439,  0.6603]],
            [[ 0.8415,  0.9093, -0.7568,  0.5403, -0.4161, -0.6536],
             [-0.7568,  0.9894, -0.5366, -0.6536, -0.1455,  0.8439]],
            [[ 0.9093, -0.7568,  0.9894, -0.4161, -0.6536, -0.1455],
             [ 0.9093, -0.7568, -0.2794, -0.4161, -0.6536,  0.9602]],
            [[ 0.1411, -0.2794, -0.5366, -0.9900,  0.9602,  0.8439],
             [ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000]]])

    ```
    """

    def __init__(self, frequency: Tensor, phase_shift: Tensor, learnable: bool = False) -> None:
        super().__init__()
        frequency = prepare_tensor_param(frequency, name="frequency")
        self.frequency = Parameter(frequency.repeat(1, 2), requires_grad=learnable)

        phase_shift = prepare_tensor_param(phase_shift, name="phase_shift")
        self.phase_shift = Parameter(phase_shift.repeat(1, 2), requires_grad=learnable)
        if self.frequency.shape != self.phase_shift.shape:
            msg = (
                f"'frequency' and 'phase_shift' shapes do not match: {self.frequency.shape} "
                f"vs {self.phase_shift.shape}"
            )
            raise RuntimeError(msg)

        self._half_size = int(frequency.shape[1])

    @property
    def input_size(self) -> int:
        r"""Return the input feature size."""
        return self.frequency.shape[0]

    @property
    def output_size(self) -> int:
        r"""Return the output feature size."""
        return self.frequency.shape[1]

    def extra_repr(self) -> str:
        return (
            f"frequency={tuple(self.frequency.shape)}, "
            f"phase_shift={tuple(self.phase_shift.shape)}, "
            f"learnable={self.frequency.requires_grad}"
        )

    def forward(self, scalar: Tensor) -> Tensor:
        features = scalar.unsqueeze(dim=-1).mul(self.frequency).add(self.phase_shift)
        return torch.cat(
            (features[..., : self._half_size].sin(), features[..., self._half_size :].cos()),
            dim=-1,
        )

    @classmethod
    def create_rand_frequency(
        cls,
        num_frequencies: int,
        min_frequency: float,
        max_frequency: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a ``CosSinNumericalEncoder`` where the frequencies are
        uniformly initialized in a frequency range.

        Args:
            num_frequencies: The number of frequencies.
            min_frequency: The minimum frequency.
            max_frequency: The maximum frequency.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are uniformly initialized in a frequency
                range.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_rand_frequency(
        ...     num_frequencies=5, min_frequency=0.1, max_frequency=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_frequency(
            num_frequencies=num_frequencies,
            min_frequency=min_frequency,
            max_frequency=max_frequency,
        )
        return cls(
            frequency=torch.rand(1, num_frequencies)
            .mul(max_frequency - min_frequency)
            .add(min_frequency),
            phase_shift=torch.zeros(1, num_frequencies),
            learnable=learnable,
        )

    @classmethod
    def create_rand_value_range(
        cls,
        num_frequencies: int,
        min_abs_value: float,
        max_abs_value: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a ``CosSinNumericalEncoder`` where the frequencies are
        uniformly initialized for a given value range.

        Args:
            num_frequencies: The number of frequencies.
            min_abs_value: The minimum absolute value to encode.
            max_abs_value: The maximum absolute value to encode.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are uniformly initialized for a given
                value range.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_rand_value_range(
        ...     num_frequencies=5, min_abs_value=0.1, max_abs_value=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_abs_range(min_abs_value=min_abs_value, max_abs_value=max_abs_value)
        return cls.create_rand_frequency(
            num_frequencies=num_frequencies,
            min_frequency=1 / max_abs_value,
            max_frequency=1 / min_abs_value,
            learnable=learnable,
        )

    @classmethod
    def create_linspace_frequency(
        cls,
        num_frequencies: int,
        min_frequency: float,
        max_frequency: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a `CosSinNumericalEncoder`` where the frequencies are
        evenly spaced in a frequency range.

        Args:
            num_frequencies: The number of frequencies.
            min_frequency: The minimum frequency.
            max_frequency: The maximum frequency.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are evenly spaced in a frequency range.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_linspace_frequency(
        ...     num_frequencies=5, min_frequency=0.1, max_frequency=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_frequency(
            num_frequencies=num_frequencies,
            min_frequency=min_frequency,
            max_frequency=max_frequency,
        )
        return cls(
            frequency=torch.linspace(start=min_frequency, end=max_frequency, steps=num_frequencies),
            phase_shift=torch.zeros(num_frequencies),
            learnable=learnable,
        )

    @classmethod
    def create_linspace_value_range(
        cls,
        num_frequencies: int,
        min_abs_value: float,
        max_abs_value: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a ``CosSinNumericalEncoder`` where the frequencies are
        evenly spaced given a value range.

        Args:
            num_frequencies: The number of frequencies.
            min_abs_value: The minimum absolute value to encode.
            max_abs_value: The maximum absolute value to encoder.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are evenly spaced.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_linspace_value_range(
        ...     num_frequencies=5, min_abs_value=0.1, max_abs_value=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_abs_range(min_abs_value=min_abs_value, max_abs_value=max_abs_value)
        return cls.create_linspace_frequency(
            num_frequencies=num_frequencies,
            min_frequency=1 / max_abs_value,
            max_frequency=1 / min_abs_value,
            learnable=learnable,
        )

    @classmethod
    def create_logspace_frequency(
        cls,
        num_frequencies: int,
        min_frequency: float,
        max_frequency: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a ``CosSinNumericalEncoder`` where the frequencies are
        evenly spaced in the log space in a frequency range.

        Args:
            num_frequencies: The number of frequencies.
            min_frequency: The minimum frequency.
            max_frequency: The maximum frequency.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are evenly spaced in the log space in a
                frequency range.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_logspace_frequency(
        ...     num_frequencies=5, min_frequency=0.1, max_frequency=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_frequency(
            num_frequencies=num_frequencies,
            min_frequency=min_frequency,
            max_frequency=max_frequency,
        )
        return cls(
            frequency=torch.logspace(
                start=math.log10(min_frequency),
                end=math.log10(max_frequency),
                steps=num_frequencies,
            ),
            phase_shift=torch.zeros(num_frequencies),
            learnable=learnable,
        )

    @classmethod
    def create_logspace_value_range(
        cls,
        num_frequencies: int,
        min_abs_value: float,
        max_abs_value: float,
        learnable: bool = False,
    ) -> CosSinNumericalEncoder:
        r"""Create a ``CosSinNumericalEncoder`` where the frequencies are
        evenly spaced in the log space given a value range.

        Args:
            num_frequencies: The number of frequencies.
            min_abs_value: The minimum absolute value to encode.
            max_abs_value: The maximum absolute value to encoder.
            learnable: If ``True`` the parameters are learnable,
                otherwise they are frozen.

        Returns:
            An instantiated ``CosSinNumericalEncoder`` where the
                frequencies are evenly spaced in the log space.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.modules import CosSinNumericalEncoder
        >>> m = CosSinNumericalEncoder.create_logspace_value_range(
        ...     num_frequencies=5, min_abs_value=0.1, max_abs_value=1.0
        ... )
        >>> m
        CosSinNumericalEncoder(frequency=(1, 10), phase_shift=(1, 10), learnable=False)

        ```
        """
        check_abs_range(min_abs_value=min_abs_value, max_abs_value=max_abs_value)
        return cls.create_logspace_frequency(
            num_frequencies=num_frequencies,
            min_frequency=1 / max_abs_value,
            max_frequency=1 / min_abs_value,
            learnable=learnable,
        )


class AsinhCosSinNumericalEncoder(CosSinNumericalEncoder):
    r"""Extension of ``CosSinNumericalEncoder`` with an additional
    feature built using the inverse hyperbolic sine (arcsinh).

    Args:
        frequency: The initial frequency values. This input should be
            a tensor of shape ``(n_features, feature_size // 2)`` or
            ``(feature_size // 2,)``.
        phase_shift: The initial phase-shift values. This input should
            be a tensor of shape ``(n_features, feature_size // 2)`` or
            ``(feature_size // 2,)``.
        learnable: If ``True`` the frequencies and phase-shift
            parameters are learnable, otherwise they are frozen.

    Shape:
        - Input: ``(*, n_features)``, where ``*`` means any number of
            dimensions.
        - Output: ``(*, n_features, feature_size + 1)``,  where ``*``
            has the same shape as the input.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.modules import AsinhCosSinNumericalEncoder
    >>> # Example with 1 feature
    >>> m = AsinhCosSinNumericalEncoder(
    ...     frequency=torch.tensor([[1.0, 2.0, 4.0]]),
    ...     phase_shift=torch.zeros(1, 3),
    ... )
    >>> m
    AsinhCosSinNumericalEncoder(frequency=(1, 6), phase_shift=(1, 6), learnable=False)
    >>> out = m(torch.tensor([[0.0], [1.0], [2.0], [3.0]]))
    >>> out
    tensor([[[ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000,  0.0000]],
            [[ 0.8415,  0.9093, -0.7568,  0.5403, -0.4161, -0.6536,  0.8814]],
            [[ 0.9093, -0.7568,  0.9894, -0.4161, -0.6536, -0.1455,  1.4436]],
            [[ 0.1411, -0.2794, -0.5366, -0.9900,  0.9602,  0.8439,  1.8184]]])
    >>> # Example with 2 features
    >>> m = AsinhCosSinNumericalEncoder(
    ...     frequency=torch.tensor([[1.0, 2.0, 4.0], [2.0, 4.0, 6.0]]),
    ...     phase_shift=torch.zeros(2, 3),
    ... )
    >>> m
    AsinhCosSinNumericalEncoder(frequency=(2, 6), phase_shift=(2, 6), learnable=False)
    >>> out = m(torch.tensor([[0.0, 3.0], [1.0, 2.0], [2.0, 1.0], [3.0, 0.0]]))
    >>> out
    tensor([[[ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000,  0.0000],
             [-0.2794, -0.5366, -0.7510,  0.9602,  0.8439,  0.6603,  1.8184]],
            [[ 0.8415,  0.9093, -0.7568,  0.5403, -0.4161, -0.6536,  0.8814],
             [-0.7568,  0.9894, -0.5366, -0.6536, -0.1455,  0.8439,  1.4436]],
            [[ 0.9093, -0.7568,  0.9894, -0.4161, -0.6536, -0.1455,  1.4436],
             [ 0.9093, -0.7568, -0.2794, -0.4161, -0.6536,  0.9602,  0.8814]],
            [[ 0.1411, -0.2794, -0.5366, -0.9900,  0.9602,  0.8439,  1.8184],
             [ 0.0000,  0.0000,  0.0000,  1.0000,  1.0000,  1.0000,  0.0000]]])

    ```
    """

    @property
    def output_size(self) -> int:
        r"""Return the output feature size."""
        return self.frequency.shape[1] + 1

    def forward(self, scalar: Tensor) -> Tensor:
        features = super().forward(scalar)
        return torch.cat(
            (features, scalar.unsqueeze(dim=-1).asinh()),
            dim=-1,
        )


def prepare_tensor_param(tensor: Tensor, name: str) -> Tensor:
    r"""Prepare a tensor parameter to be a 2d tensor.

    Args:
        tensor: The tensor to prepare.
        name: The name associated to the tensor.

    Returns:
        The prepared tensor.

    Raises:
        RuntimeError: if the input tensor is not a 1d or 2d tensor.
    """
    if tensor.ndim == 1:
        tensor = tensor.view(1, -1)
    if tensor.ndim != 2:
        msg = f"Incorrect shape for '{name}': {tensor.shape}"
        raise RuntimeError(msg)
    return tensor


def check_abs_range(min_abs_value: float, max_abs_value: float) -> None:
    r"""Check the frequency parameters.

    Args:
        min_abs_value: The minimum absolute value to encode.
        max_abs_value: The maximum absolute value to encode.

    Raises:
        RuntimeError: if one of the parameters is invalid.
    """
    if min_abs_value <= 0:
        msg = f"'min_abs_value' has to be greater than 0 (received: {min_abs_value})"
        raise RuntimeError(msg)
    if max_abs_value < min_abs_value:
        msg = (
            f"'max_abs_value' (received: {max_abs_value}) has to be greater than "
            f"'min_abs_value' (received: {min_abs_value})"
        )
        raise RuntimeError(msg)


def check_frequency(
    num_frequencies: int,
    min_frequency: float,
    max_frequency: float,
) -> None:
    r"""Check the frequency parameters.

    Args:
        num_frequencies: The number of frequencies.
        min_frequency: The minimum frequency.
        max_frequency: The maximum frequency.

    Raises:
        RuntimeError: if one of the parameters is invalid.
    """
    if num_frequencies < 1:
        msg = f"'num_frequencies' has to be greater or equal to 1 (received: {num_frequencies})"
        raise RuntimeError(msg)
    if min_frequency <= 0:
        msg = f"'min_frequency' has to be greater than 0 (received: {min_frequency})"
        raise RuntimeError(msg)
    if max_frequency < min_frequency:
        msg = (
            f"'max_frequency' (received: {max_frequency}) has to be greater than "
            f"'min_frequency' (received: {min_frequency})"
        )
        raise RuntimeError(msg)
