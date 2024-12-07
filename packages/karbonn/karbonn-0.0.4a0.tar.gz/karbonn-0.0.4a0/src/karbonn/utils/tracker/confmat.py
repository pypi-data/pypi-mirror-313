r"""Contain confusion matrices for binary labels and multiclass
labels."""

from __future__ import annotations

__all__ = [
    "BaseConfusionMatrixTracker",
    "BinaryConfusionMatrixTracker",
    "MulticlassConfusionMatrixTracker",
    "str_binary_confusion_matrix",
]

from typing import TYPE_CHECKING, Any

import torch
from minrecord import BaseRecord, MaxScalarRecord, MinScalarRecord
from torch import Tensor

from karbonn.distributed.ddp import SUM, sync_reduce
from karbonn.utils.format import str_table
from karbonn.utils.tracker.exception import EmptyTrackerError

try:
    from typing import Self  # Introduced in python 3.11
except ImportError:  # pragma: no cover
    from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


class BaseConfusionMatrixTracker:
    r"""Define the base class to implement confusion matrix.

    Args:
        matrix: The initial confusion matrix values as a
            ``torch.Tensor`` of type long and shape
            ``(num_classes, num_classes)``. The rows indicate the true
            labels and the columns indicate the predicted labels.
    """

    def __init__(self, matrix: Tensor) -> None:
        check_confusion_matrix(matrix)
        self._matrix = matrix
        self._count = self._compute_count()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(count={self.count:,}, "
            f"shape={self._matrix.shape}, dtype={self._matrix.dtype})"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(num_classes={self.num_classes:,}, "
            f"count={self.count:,})"
        )

    @property
    def count(self) -> int:
        r"""The number of examples in the tracker since the last reset.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.count
        6

        ```
        """
        return self._count

    @property
    def matrix(self) -> Tensor:
        r"""Get the confusion matrix values as a ``torch.Tensor`` of type
        long and shape ``(num_classes, num_classes)``.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.matrix
        tensor([[2, 0],
                [1, 3]])

        ```
        """
        return self._matrix

    @property
    def num_classes(self) -> int:
        r"""Get the number of classes.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.num_classes
        2

        ```
        """
        return self._matrix.shape[0]

    def all_reduce(self) -> Self:
        r"""Reduce the values across all machines in such a way that all
        get the final result.

        The confusion matrix is reduced by summing all the confusion
        matrices (1 confusion matrix per distributed process).

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat_reduced = confmat.all_reduce()

        ```
        """
        return self.__class__(sync_reduce(self._matrix, SUM))

    def get_normalized_matrix(self, normalization: str) -> Tensor:
        r"""Get the normalized confusion matrix.

        Args:
            normalization: The normalization strategy.
                The supported normalization strategies are:

                    - ``'true'``: normalization over the targets
                        (most commonly used)
                    - ``'pred'``: normalization over the predictions
                    - ``'all'``: normalization over the whole matrix

        Returns:
            The normalized confusion matrix as ``torch.Tensor`` of
                type float and shape ``(num_classes, num_classes)``.

        Raises:
            ValueError: if the normalization strategy is not supported.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.get_normalized_matrix(normalization="true")
        tensor([[1.0000, 0.0000],
                [0.2500, 0.7500]])
        >>> confmat.get_normalized_matrix(normalization="pred")
        tensor([[0.6667, 0.0000],
                [0.3333, 1.0000]])
        >>> confmat.get_normalized_matrix(normalization="all")
        tensor([[0.3333, 0.0000],
                [0.1667, 0.5000]])

        ```
        """
        if normalization == "true":
            # Clamp by a small value to avoid division by 0
            return self.matrix / self.matrix.sum(dim=1, keepdim=True).clamp(min=1e-8)
        if normalization == "pred":
            # Clamp by a small value to avoid division by 0
            return self.matrix / self.matrix.sum(dim=0, keepdim=True).clamp(min=1e-8)
        if normalization == "all":
            # Clamp by a small value to avoid division by 0
            return self.matrix / self.matrix.sum().clamp(min=1e-8)
        msg = (
            f"Incorrect normalization: {normalization}. The supported normalization strategies "
            "are `true`, `pred` and `all`"
        )
        raise ValueError(msg)

    def reset(self) -> None:
        r"""Reset the confusion matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.count
        6
        >>> confmat.reset()
        >>> confmat.count
        0

        ```
        """
        self._matrix.zero_()
        self._count = 0

    def update(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the confusion matrix with new predictions.

        Args:
            prediction: The predicted labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.
            target: The ground truth labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker()
        >>> confmat.update(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  2                ┃ [FP]  0                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  3                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=6

        ```
        """
        self._matrix += (
            torch.bincount(
                (target.flatten() * self.num_classes + prediction.flatten()).long(),
                minlength=self.num_classes**2,
            )
            .reshape(self.num_classes, self.num_classes)
            .to(device=self._matrix.device)
        )
        self._count = self._compute_count()

    def _compute_count(self) -> int:
        return self._matrix.sum().item()


class BinaryConfusionMatrixTracker(BaseConfusionMatrixTracker):
    r"""Implement a confusion matrix for binary labels.

    Args:
        matrix: The initial confusion matrix values as a
            ``torch.Tensor`` of type long and shape ``(2, 2)``.
            The structure of the matrix is:

                    predicted label
                        TN | FP
            true label  -------
                        FN | TP

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
    >>> confmat = BinaryConfusionMatrixTracker()
    >>> confmat
    ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual negative (0) ┃ [TN]  0                ┃ [FP]  0                ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual positive (1) ┃ [FN]  0                ┃ [TP]  0                ┃
    ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
    count=0
    >>> confmat.update(
    ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
    ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
    ... )
    >>> confmat
    ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual negative (0) ┃ [TN]  2                ┃ [FP]  0                ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  3                ┃
    ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
    count=6
    >>> confmat.matrix
    tensor([[2, 0],
            [1, 3]])
    >>> confmat.count
    6
    >>> confmat.num_classes
    2

    ```
    """

    def __init__(self, matrix: Tensor | None = None) -> None:
        if matrix is None:
            matrix = torch.zeros(2, 2, dtype=torch.long)
        if matrix.shape != (2, 2):
            msg = f"Incorrect shape. Expected a (2, 2) matrix but received {matrix.shape}"
            raise ValueError(msg)
        super().__init__(matrix)

    def __repr__(self) -> str:
        return "\n".join(
            [
                str_binary_confusion_matrix(self._matrix),
                f"count={self.count:,}",
            ]
        )

    def clone(self) -> Self:
        r"""Create a copy of the current confusion matrix matrix.

        Returns:
            A copy of the current confusion matrix matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat_cloned = confmat.clone()
        >>> confmat.update(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]), target=torch.tensor([0, 1, 1, 0, 0, 1])
        ... )
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  4                ┃ [FP]  1                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  6                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=12
        >>> confmat_cloned
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  2                ┃ [FP]  0                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  3                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=6

        ```
        """
        return self.__class__(self.matrix.clone())

    def equal(self, other: Any) -> bool:
        r"""Indicate if two confusion matrices are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the confusion matrices are equal,
                ``False`` otherwise.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.equal(confmat2)
        False

        ```
        """
        if not isinstance(other, BinaryConfusionMatrixTracker):
            return False
        return self.matrix.equal(other.matrix)

    @classmethod
    def from_predictions(cls, prediction: Tensor, target: Tensor) -> Self:
        r"""Create a confusion matrix given ground truth and predicted
        labels.

        Args:
            prediction: The predicted labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.
            target: The ground truth labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  2                ┃ [FP]  0                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  3                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=6

        ```
        """
        confmat = cls()
        confmat.update(prediction, target)
        return confmat

    ##########################
    #     Transformation     #
    ##########################

    def __add__(self, other: Any) -> Self:
        return self.add(other)

    def __iadd__(self, other: Any) -> Self:
        self.add_(other)
        return self

    def __sub__(self, other: Any) -> Self:
        return self.sub(other)

    def add(self, other: Self) -> Self:
        r"""Add a confusion matrix.

        Args:
            other: The other confusion matrix to add.

        Returns:
            A new confusion matrix containing the addition of the two
                confusion matrices.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat1 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat = confmat1.add(confmat2)
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  4                ┃ [FP]  1                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  6                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=12

        ```
        """
        check_op_compatibility_binary(self, other, "add")
        return self.__class__(self.matrix.add(other.matrix))

    def add_(self, other: Self) -> None:
        r"""Add a confusion matrix.

        In-place version of ``add``.

        Args:
            other: The other confusion matrix to add.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.add_(confmat2)
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  4                ┃ [FP]  1                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  6                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=12

        ```
        """
        check_op_compatibility_binary(self, other, "add")
        self.matrix.add_(other.matrix)
        self._count = self._compute_count()

    def merge(self, matrices: Iterable[Self]) -> Self:
        r"""Merge several matrices with the current matrix and returns a
        new matrix.

        Args:
            matrices: The matrices to merge to the current matrix.

        Returns:
            The merged matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat1 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat = confmat.merge([confmat1, confmat2])
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  6                ┃ [FP]  1                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  2                ┃ [TP]  9                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=18

        ```
        """
        output = self.clone()
        for matrix in matrices:
            output.add_(matrix)
        return output

    def merge_(self, matrices: Iterable[Self]) -> None:
        r"""Merge several matrices into the current matrix.

        In-place version of ``merge``.

        Args:
            matrices: The matrices to merge to the current matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat1 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.merge_([confmat1, confmat2])
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  6                ┃ [FP]  1                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  2                ┃ [TP]  9                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=18

        ```
        """
        for matrix in matrices:
            self.add_(matrix)

    def sub(self, other: Self) -> Self:
        r"""Subtract a confusion matrix.

        Args:
            other: The other confusion matrix to subtract.

        Returns:
            A new confusion matrix containing the difference of the
                two confusion  matrices.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat1 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat2 = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([1, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([0, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat = confmat1.sub(confmat2)
        >>> confmat
        ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual negative (0) ┃ [TN]  2                ┃ [FP]  0                ┃
        ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃ actual positive (1) ┃ [FN]  1                ┃ [TP]  3                ┃
        ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛
        count=6

        ```
        """
        check_op_compatibility_binary(self, other, "sub")
        return self.__class__(self.matrix.sub(other.matrix))

    ###################
    #     Metrics     #
    ###################

    @property
    def false_negative(self) -> int:
        r"""Get the false negative i.e. the number of incorrectly
        classified negative examples.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.false_negative
        1

        ```
        """
        return self._matrix[1, 0].item()

    @property
    def false_positive(self) -> int:
        r"""Get the false positive i.e. the number of incorrectly
        classified positive examples.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.false_positive
        0

        ```
        """
        return self._matrix[0, 1].item()

    @property
    def negative(self) -> int:
        r"""Get the number of negative true labels.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.negative
        2

        ```
        """
        return self.true_negative + self.false_positive

    @property
    def positive(self) -> int:
        r"""Get the number of positive true labels.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.positive
        4

        ```
        """
        return self.true_positive + self.false_negative

    @property
    def predictive_negative(self) -> int:
        r"""Get the number of negative predictions.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.predictive_negative
        3

        ```
        """
        return self.false_negative + self.true_negative

    @property
    def predictive_positive(self) -> int:
        r"""Get the number of positive predictions.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.predictive_positive
        3

        ```
        """
        return self.true_positive + self.false_positive

    @property
    def true_negative(self) -> int:
        r"""Get the true negative i.e. the number of correctly classified
        negative examples.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.true_negative
        2

        ```
        """
        return self._matrix[0, 0].item()

    @property
    def true_positive(self) -> int:
        r"""Get the true positive i.e. the number of correctly classified
        positive examples.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.true_positive
        3

        ```
        """
        return self._matrix[1, 1].item()

    def accuracy(self) -> float:
        r"""Compute the accuracy.

        Returns:
            The accuracy.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.accuracy()
        0.833333...

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the accuracy because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        return float(self.true_positive + self.true_negative) / float(self._count)

    def balanced_accuracy(self) -> float:
        r"""Compute the balanced accuracy.

        Returns:
            The balanced accuracy.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.balanced_accuracy()
        0.875

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the balanced accuracy because the confusion matrix "
                "is empty"
            )
            raise EmptyTrackerError(msg)
        return (self.true_negative_rate() + self.true_positive_rate()) / 2

    def f_beta_score(self, beta: float = 1.0) -> float:
        r"""Compute the F-beta score.

        Args:
            beta: The beta value.

        Returns:
            The F-beta score.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.f_beta_score()
        0.857142...
        >>> confmat.f_beta_score(2)
        0.789473...

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the F-beta score because the confusion matrix "
                "is empty"
            )
            raise EmptyTrackerError(msg)
        beta2 = beta**2
        if self.true_positive == 0:
            return 0.0
        return ((1.0 + beta2) * self.true_positive) / (
            (1.0 + beta2) * self.true_positive + beta2 * self.false_negative + self.false_positive
        )

    def false_negative_rate(self) -> float:
        r"""Compute the false negative rate i.e. the miss rate.

        Returns:
            The false negative rate.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.false_negative_rate()
        0.25

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the false negative rate because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        if self.positive == 0:
            return 0.0
        return float(self.false_negative) / float(self.positive)

    def false_positive_rate(self) -> float:
        r"""Compute the false positive rate i.e. the probability of false
        alarm.

        Returns:
            The false positive rate.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.false_positive_rate()
        0.0

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the false positive rate because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        if self.negative == 0:
            return 0.0
        return float(self.false_positive) / float(self.negative)

    def jaccard_index(self) -> float:
        r"""Compute the Jaccard index.

        Returns:
            The Jaccard index.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.jaccard_index()
        0.75

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the Jaccard index because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        if self.true_positive == 0:
            return 0.0
        return float(self.true_positive) / float(
            self.true_positive + self.false_negative + self.false_positive
        )

    def precision(self) -> float:
        r"""Compute the precision.

        Returns:
            The precision.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.precision()
        1.0

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the precision because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        if self.predictive_positive == 0:
            return 0.0
        return float(self.true_positive) / float(self.predictive_positive)

    def recall(self) -> float:
        r"""Compute the recall i.e. the probability of positive
        detection.

        Returns:
            The recall.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.recall()
        0.75

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the recall because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        if self.positive == 0:
            return 0.0
        return float(self.true_positive) / float(self.positive)

    def true_negative_rate(self) -> float:
        r"""Compute the true negative rate.

        Returns:
            The true negative rate.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.true_negative_rate()
        1.0

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the true negative rate because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        if self.negative == 0:
            return 0.0
        return float(self.true_negative) / float(self.negative)

    def true_positive_rate(self) -> float:
        r"""Compute the true positive rate.

        Returns:
            The true positive rate.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.true_positive_rate()
        0.75

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the true positive rate because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        return self.recall()

    def compute_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float]:
        r"""Compute all the metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 1, 0, 0, 1]),
        ...     target=torch.tensor([1, 1, 1, 0, 0, 1]),
        ... )
        >>> confmat.compute_metrics()
        {'accuracy': 0.833333...,
         'balanced_accuracy': 0.875,
         'false_negative_rate': 0.25,
         'false_negative': 1,
         'false_positive_rate': 0.0,
         'false_positive': 0,
         'jaccard_index': 0.75,
         'count': 6,
         'precision': 1.0,
         'recall': 0.75,
         'true_negative_rate': 1.0,
         'true_negative': 2,
         'true_positive_rate': 0.75,
         'true_positive': 3,
         'f1_score': 0.857142...}

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the metrics because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        metrics = {
            f"{prefix}accuracy{suffix}": self.accuracy(),
            f"{prefix}balanced_accuracy{suffix}": self.balanced_accuracy(),
            f"{prefix}false_negative_rate{suffix}": self.false_negative_rate(),
            f"{prefix}false_negative{suffix}": self.false_negative,
            f"{prefix}false_positive_rate{suffix}": self.false_positive_rate(),
            f"{prefix}false_positive{suffix}": self.false_positive,
            f"{prefix}jaccard_index{suffix}": self.jaccard_index(),
            f"{prefix}count{suffix}": self.count,
            f"{prefix}precision{suffix}": self.precision(),
            f"{prefix}recall{suffix}": self.recall(),
            f"{prefix}true_negative_rate{suffix}": self.true_negative_rate(),
            f"{prefix}true_negative{suffix}": self.true_negative,
            f"{prefix}true_positive_rate{suffix}": self.true_positive_rate(),
            f"{prefix}true_positive{suffix}": self.true_positive,
        }
        for beta in betas:
            metrics[f"{prefix}f{beta}_score{suffix}"] = self.f_beta_score(beta)
        return metrics

    def get_records(
        self, betas: Sequence[float] = (1,), prefix: str = "", suffix: str = ""
    ) -> tuple[BaseRecord, ...]:
        r"""Get the records associated to each metric.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            The records.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import BinaryConfusionMatrixTracker
        >>> confmat = BinaryConfusionMatrixTracker()
        >>> confmat.get_records()
        (MaxScalarRecord(name=accuracy, max_size=10, size=0),
         MaxScalarRecord(name=balanced_accuracy, max_size=10, size=0),
         MaxScalarRecord(name=jaccard_index, max_size=10, size=0),
         MaxScalarRecord(name=precision, max_size=10, size=0),
         MaxScalarRecord(name=recall, max_size=10, size=0),
         MaxScalarRecord(name=true_negative_rate, max_size=10, size=0),
         MaxScalarRecord(name=true_negative, max_size=10, size=0),
         MaxScalarRecord(name=true_positive_rate, max_size=10, size=0),
         MaxScalarRecord(name=true_positive, max_size=10, size=0),
         MinScalarRecord(name=false_negative_rate, max_size=10, size=0),
         MinScalarRecord(name=false_negative, max_size=10, size=0),
         MinScalarRecord(name=false_positive_rate, max_size=10, size=0),
         MinScalarRecord(name=false_positive, max_size=10, size=0),
         MaxScalarRecord(name=f1_score, max_size=10, size=0))

        ```
        """
        trackers = [
            MaxScalarRecord(name=f"{prefix}accuracy{suffix}"),
            MaxScalarRecord(name=f"{prefix}balanced_accuracy{suffix}"),
            MaxScalarRecord(name=f"{prefix}jaccard_index{suffix}"),
            MaxScalarRecord(name=f"{prefix}precision{suffix}"),
            MaxScalarRecord(name=f"{prefix}recall{suffix}"),
            MaxScalarRecord(name=f"{prefix}true_negative_rate{suffix}"),
            MaxScalarRecord(name=f"{prefix}true_negative{suffix}"),
            MaxScalarRecord(name=f"{prefix}true_positive_rate{suffix}"),
            MaxScalarRecord(name=f"{prefix}true_positive{suffix}"),
            MinScalarRecord(name=f"{prefix}false_negative_rate{suffix}"),
            MinScalarRecord(name=f"{prefix}false_negative{suffix}"),
            MinScalarRecord(name=f"{prefix}false_positive_rate{suffix}"),
            MinScalarRecord(name=f"{prefix}false_positive{suffix}"),
        ]
        return tuple(
            trackers + [MaxScalarRecord(name=f"{prefix}f{beta}_score{suffix}") for beta in betas]
        )


class MulticlassConfusionMatrixTracker(BaseConfusionMatrixTracker):
    r"""Implement a confusion matrix for multiclass labels.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
    >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
    ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
    ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
    ... )
    >>> confmat.matrix
    tensor([[2, 1, 0],
            [0, 0, 0],
            [1, 1, 1]])
    >>> confmat.count
    6
    >>> confmat.num_classes
    3

    ```
    """

    def auto_update(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the confusion matrix with new predictions.

        Unlike ``update``, this method will update the number of
        classes if a larger number of classes if found. This method
        allows to use confusion matrix in the setting where the number
        of classes is unknown at the beginning of the process.

        Args:
            prediction: The predicted labels as a ``torch.Tensor``
                of type long and shape ``(d0, d1, ..., dn)``.
            target: The ground truth labels as a ``torch.Tensor``
                of type long and shape ``(d0, d1, ..., dn)``.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.matrix
        tensor([[2, 1, 0],
                [0, 0, 0],
                [1, 1, 1]])
        >>> confmat.auto_update(
        ...     prediction=torch.tensor([2, 3, 2, 1, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 3, 3, 3]),
        ... )

        ```
        """
        # +1 because it is 0-indexed
        num_classes = max(prediction.max().item(), target.max().item()) + 1
        if num_classes > self.num_classes:
            self.resize(num_classes)
        self.update(prediction, target)

    def clone(self) -> Self:
        r"""Create a copy of the current confusion matrix matrix.

        Returns:
            A copy of the current confusion matrix matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat_cloned = confmat.clone()
        >>> confmat.update(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat.matrix
        tensor([[4, 1, 1],
                [1, 0, 1],
                [1, 1, 2]])
        >>> confmat_cloned.matrix
        tensor([[2, 1, 0],
                [0, 0, 0],
                [1, 1, 1]])

        ```
        """
        return self.__class__(self.matrix.clone())

    def equal(self, other: Any) -> bool:
        r"""Indicate if two confusion matrices are equal or not.

        Args:
            other: The value to compare.

        Returns:
            ``True`` if the confusion matrices are equal,
                ``False`` otherwise.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat1 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat1.equal(confmat2)
        False

        ```
        """
        if not isinstance(other, MulticlassConfusionMatrixTracker):
            return False
        return self.matrix.equal(other.matrix)

    def resize(self, num_classes: int) -> None:
        r"""Resize the current confusion matrix to a larger number of
        classes.

        Args:
            num_classes: The new number of classes.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.matrix
        tensor([[2, 1, 0],
                [0, 0, 0],
                [1, 1, 1]])
        >>> confmat.resize(5)
        >>> confmat.matrix
        tensor([[2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]])

        ```
        """
        if num_classes < self.num_classes:
            msg = (
                f"Incorrect number of classes: {num_classes}. The confusion matrix "
                f"(num_classes={self.num_classes}) can be resized only to a larger number "
                "of classes"
            )
            raise ValueError(msg)
        matrix = self._matrix
        self._matrix = torch.zeros(num_classes, num_classes, dtype=torch.long)
        self._matrix[: matrix.shape[0], : matrix.shape[1]] = matrix

    @classmethod
    def from_num_classes(cls, num_classes: int) -> Self:
        r"""Create a confusion matrix given the number of classes.

        Args:
            num_classes: The number of classes.

        Returns:
            An instantiated confusion matrix for the given number of
                classes.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_num_classes(5)
        >>> confmat.matrix
        tensor([[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]])

        ```
        """
        if num_classes < 1:
            msg = (
                "Incorrect number of classes. `num_classes` has to be greater or equal to 1 but "
                f"received {num_classes}"
            )
            raise ValueError(msg)
        return cls(matrix=torch.zeros(num_classes, num_classes, dtype=torch.long))

    @classmethod
    def from_predictions(cls, prediction: Tensor, target: Tensor) -> Self:
        r"""Create a confusion matrix given ground truth and predicted
        labels.

        Note: the number of classes is inferred from the maximum
        ground truth and predicted labels.

        Args:
            prediction: The predicted labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.
            target: The ground truth labels as a ``torch.Tensor`` of
                type long and shape ``(d0, d1, ..., dn)``.

        Returns:
            An instantiated confusion matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.matrix
        tensor([[2, 1, 0],
                [0, 0, 0],
                [1, 1, 1]])

        ```
        """
        # use a fake number of classes. `auto_update` will find the right number of classes
        confmat = cls.from_num_classes(num_classes=1)
        confmat.auto_update(prediction, target)
        return confmat

    ##########################
    #     Transformation     #
    ##########################

    def __add__(self, other: Any) -> Self:
        return self.add(other)

    def __iadd__(self, other: Any) -> Self:
        self.add_(other)
        return self

    def __sub__(self, other: Any) -> Self:
        return self.sub(other)

    def add(self, other: Self) -> Self:
        r"""Add a confusion matrix.

        Args:
            other: The other confusion matrix to add.

        Returns:
            A new confusion matrix containing the addition of the two
                confusion matrices.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat1 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat = confmat1.add(confmat2)
        >>> confmat.matrix
        tensor([[4, 1, 1],
                [1, 0, 1],
                [1, 1, 2]])

        ```
        """
        check_op_compatibility_multiclass(self, other, "add")
        return self.__class__(self.matrix.add(other.matrix))

    def add_(self, other: MulticlassConfusionMatrixTracker) -> None:
        r"""Add a confusion matrix.

        In-place version of ``add``.

        Args:
            other: The other confusion matrix to add.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat.add_(confmat2)
        >>> confmat.matrix
        tensor([[4, 1, 1],
                [1, 0, 1],
                [1, 1, 2]])

        ```
        """
        check_op_compatibility_multiclass(self, other, "add")
        self.matrix.add_(other.matrix)
        self._count = self._compute_count()

    def merge(self, matrices: Iterable[Self]) -> Self:
        r"""Merge several matrices with the current matrix and returns a
        new matrix.

        Args:
            matrices: The matrices to merge to the current matrix.

        Returns:
            The merged matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat1 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat = confmat.merge([confmat1, confmat2])
        >>> confmat.matrix
        tensor([[6, 2, 1],
                [1, 0, 1],
                [2, 2, 3]])

        ```
        """
        output = self.clone()
        for matrix in matrices:
            output.add_(matrix)
        return output

    def merge_(self, matrices: Iterable[Self]) -> None:
        r"""Merge several matrices into the current matrix.

        In-place version of ``merge``.

        Args:
            matrices: The matrices to merge to the current matrix.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat1 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat.merge_([confmat1, confmat2])
        >>> confmat.matrix
        tensor([[6, 2, 1],
                [1, 0, 1],
                [2, 2, 3]])

        ```
        """
        for matrix in matrices:
            self.add_(matrix)

    def sub(self, other: Self) -> Self:
        r"""Subtract a confusion matrix.

        Args:
            other: The other confusion matrix to subtract.

        Returns:
            A new confusion matrix containing the difference of the
                two confusion matrices.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat1 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1, 2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0, 0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat2 = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([2, 2, 2, 0, 0, 0]),
        ...     target=torch.tensor([0, 1, 2, 0, 0, 1]),
        ... )
        >>> confmat = confmat1.sub(confmat2)
        >>> confmat.matrix
        tensor([[2, 1, 0],
                [0, 0, 0],
                [1, 1, 1]])

        ```
        """
        check_op_compatibility_multiclass(self, other, "sub")
        return self.__class__(self.matrix.sub(other.matrix))

    ###################
    #     Metrics     #
    ###################

    @property
    def false_negative(self) -> Tensor:
        r"""Get the false negative as a ``torch.Tensor`` of type long and
        shape ``(num_classes,)``.

        The number of false negative for each class i.e. the elements
        that have been labelled as negative by the model, but they are
        actually positive.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.false_negative
        tensor([1, 0, 2])

        ```
        """
        return self.support - self.true_positive

    @property
    def false_positive(self) -> Tensor:
        r"""Get the false positive as a ``torch.Tensor`` of type long and
        shape ``(num_classes,)``.

        The number of false positive for each class i.e. the elements
        that have been labelled as positive by the model, but they are
        actually negative.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.false_positive
        tensor([1, 2, 0])

        ```
        """
        return self.matrix.sum(dim=0) - self.true_positive

    @property
    def support(self) -> Tensor:
        r"""Get the support as a ``torch.Tensor`` of type long and shape
        ``(num_classes,)``.

        The support for each class i.e. the number of elements for a
        given class (true label).

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.support
        tensor([3, 0, 3])

        ```
        """
        return self.matrix.sum(dim=1)

    @property
    def true_positive(self) -> Tensor:
        r"""Get the true positive as a ``torch.Tensor`` of type long and
        shape ``(num_classes,)``.

        The number of true positive for each class i.e. the elements
        that have been labelled as positive by the model, and they are
        actually positive.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.true_positive
        tensor([2, 0, 1])

        ```
        """
        return self.matrix.diag()

    def accuracy(self) -> float:
        r"""Compute the accuracy.

        Returns:
            The accuracy.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.accuracy()
        0.5

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the accuracy because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        return float(self.true_positive.sum().item()) / float(self._count)

    def balanced_accuracy(self) -> float:
        r"""Compute the balanced accuracy.

        Returns:
            The balanced accuracy.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.balanced_accuracy()
        0.333333...

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the balanced accuracy because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        return self.recall().mean().item()

    def f_beta_score(self, beta: float = 1.0) -> Tensor:
        r"""Compute the F-beta score for each class.

        Args:
            beta: The beta value.

        Returns:
            The F-beta score for each class as a ``torch.Tensor`` of
                type float and shape ``(num_classes,)``

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.f_beta_score()
        tensor([0.6667, 0.0000, 0.5000])
        >>> confmat.f_beta_score(2)
        tensor([0.6667, 0.0000, 0.3846])

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the F-beta score because the confusion matrix "
                "is empty"
            )
            raise EmptyTrackerError(msg)
        beta2 = beta**2
        return (self.true_positive.mul(1.0 + beta2)) / (
            self.true_positive.mul(1.0 + beta2)
            + self.false_negative.mul(beta2)
            + self.false_positive
        )

    def macro_f_beta_score(self, beta: float = 1.0) -> float:
        r"""Compute the macro (a.k.a. unweighted mean) F-beta score.

        Args:
            beta: The beta value.

        Returns:
            The macro F-beta score.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.macro_f_beta_score()
        0.388888...
        >>> confmat.macro_f_beta_score(2)
        0.350427...

        ```
        """
        return self.f_beta_score(beta).mean().item()

    def micro_f_beta_score(self, beta: float = 1.0) -> float:
        r"""Compute the micro F-beta score.

        Args:
            beta: The beta value.

        Returns:
            The micro F-beta score.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.micro_f_beta_score()
        0.5
        >>> confmat.micro_f_beta_score(2)
        0.5

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the micro F-beta score because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        beta2 = beta**2
        return (
            (self.true_positive.sum().mul(1.0 + beta2))
            / (
                self.true_positive.sum().mul(1.0 + beta2)
                + self.false_negative.sum().mul(beta2)
                + self.false_positive.sum()
            )
        ).item()

    def weighted_f_beta_score(self, beta: float = 1.0) -> float:
        r"""Compute the weighted mean F-beta score.

        Args:
            beta: The beta value.

        Returns:
            The weighted mean F-beta score.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.weighted_f_beta_score()
        0.583333...
        >>> confmat.weighted_f_beta_score(2)
        0.525641...

        ```
        """
        return self.f_beta_score(beta).mul(self.support).sum().item() / float(self._count)

    def precision(self) -> Tensor:
        r"""Compute the precision for each class.

        Returns:
            The precision for each class as a ``torch.Tensor`` of type
                float and shape ``(num_classes,)``.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.precision()
        tensor([0.6667, 0.0000, 1.0000])

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the precision because the confusion matrix is empty"
            )
            raise EmptyTrackerError(msg)
        return self.true_positive.float().div(self.matrix.sum(dim=0).clamp(min=1e-8))

    def macro_precision(self) -> float:
        r"""Compute the macro (a.k.a. unweighted mean) precision.

        Returns:
            The macro precision.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.macro_precision()
        0.555555...

        ```
        """
        return self.precision().mean().item()

    def micro_precision(self) -> float:
        r"""Compute the micro precision.

        Returns:
            The micro precision.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.micro_precision()
        0.5...

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the micro precision because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        return (
            self.true_positive.sum()
            .div(self.true_positive.sum().add(self.false_positive.sum()))
            .item()
        )

    def weighted_precision(self) -> float:
        r"""Compute the weighted mean (a.k.a. unweighted mean) precision.

        Returns:
            The weighted mean precision.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.weighted_precision()
        0.833333...

        ```
        """
        return self.precision().mul(self.support).sum().item() / float(self._count)

    def recall(self) -> Tensor:
        r"""Compute the recall for each class.

        Returns:
            The recall for each class as a ``torch.Tensor`` of type
                float and shape ``(num_classes,)``.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.recall()
        tensor([0.6667, 0.0000, 0.3333])

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the recall because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        return self.true_positive.float().div(self.support.clamp(min=1e-8))

    def macro_recall(self) -> float:
        r"""Compute the macro (a.k.a. unweighted mean) recall.

        Returns:
            The macro recall.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.macro_recall()
        0.333333...

        ```
        """
        return self.recall().mean().item()

    def micro_recall(self) -> float:
        r"""Compute the micro recall.

        Returns:
            The micro recall.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.micro_recall()
        0.5

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the micro recall because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        return (
            self.true_positive.sum()
            .div(self.true_positive.sum().add(self.false_negative.sum()))
            .item()
        )

    def weighted_recall(self) -> float:
        r"""Compute the weighted mean (a.k.a. unweighted mean) recall.

        Returns:
            The weighted mean recall.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.weighted_precision()
        0.833333...

        ```
        """
        return self.recall().mul(self.support).sum().item() / float(self._count)

    def compute_per_class_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, Tensor]:
        r"""Compute all the per-class metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the per-class metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_per_class_metrics()
        {'precision': tensor([0.6667, 0.0000, 1.0000]),
         'recall': tensor([0.6667, 0.0000, 0.3333]),
         'f1_score': tensor([0.6667, 0.0000, 0.5000])}

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the metrics because the confusion matrix is empty"
            raise EmptyTrackerError(msg)

        metrics = {
            f"{prefix}precision{suffix}": self.precision(),
            f"{prefix}recall{suffix}": self.recall(),
        }
        for beta in betas:
            metrics[f"{prefix}f{beta}_score{suffix}"] = self.f_beta_score(beta)
        return metrics

    def compute_macro_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float]:
        r"""Compute all the "macro" metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the "macro" metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_macro_metrics()
        {'macro_precision': 0.555555...,
         'macro_recall': 0.333333...,
         'macro_f1_score': 0.388888...}

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the 'macro' metrics because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        metrics = {
            f"{prefix}macro_precision{suffix}": self.macro_precision(),
            f"{prefix}macro_recall{suffix}": self.macro_recall(),
        }
        for beta in betas:
            metrics[f"{prefix}macro_f{beta}_score{suffix}"] = self.macro_f_beta_score(beta)
        return metrics

    def compute_micro_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float]:
        r"""Compute all the "micro" metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the "micro" metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_micro_metrics()
        {'micro_precision': 0.5,
         'micro_recall': 0.5,
         'micro_f1_score': 0.5}

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the 'micro' metrics because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        metrics = {
            f"{prefix}micro_precision{suffix}": self.micro_precision(),
            f"{prefix}micro_recall{suffix}": self.micro_recall(),
        }
        for beta in betas:
            metrics[f"{prefix}micro_f{beta}_score{suffix}"] = self.micro_f_beta_score(beta)
        return metrics

    def compute_weighted_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float]:
        r"""Compute all the "weighted" metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the "weighted" metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_weighted_metrics()
        {'weighted_precision': 0.833333...,
         'weighted_recall': 0.5,
         'weighted_f1_score': 0.583333...}

        ```
        """
        if self.count == 0:
            msg = (
                "It is not possible to compute the 'weighted' metrics because the confusion "
                "matrix is empty"
            )
            raise EmptyTrackerError(msg)
        metrics = {
            f"{prefix}weighted_precision{suffix}": self.weighted_precision(),
            f"{prefix}weighted_recall{suffix}": self.weighted_recall(),
        }
        for beta in betas:
            metrics[f"{prefix}weighted_f{beta}_score{suffix}"] = self.weighted_f_beta_score(beta)
        return metrics

    def compute_scalar_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float]:
        r"""Compute all the scalar metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the scalar metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_scalar_metrics()
        {'accuracy': 0.5,
         'balanced_accuracy': 0.333333...,
         'count': 6,
         'macro_precision': 0.555555...,
         'macro_recall': 0.333333...,
         'macro_f1_score': 0.388888...,
         'micro_precision': 0.5,
         'micro_recall': 0.5,
         'micro_f1_score': 0.5,
         'weighted_precision': 0.833333...,
         'weighted_recall': 0.5,
         'weighted_f1_score': 0.583333...}

        ```
        """
        if self.count == 0:
            msg = "It is not possible to compute the metrics because the confusion matrix is empty"
            raise EmptyTrackerError(msg)
        metrics = {
            f"{prefix}accuracy{suffix}": self.accuracy(),
            f"{prefix}balanced_accuracy{suffix}": self.balanced_accuracy(),
            f"{prefix}count{suffix}": self.count,
        }
        metrics.update(self.compute_macro_metrics(betas, prefix, suffix))
        metrics.update(self.compute_micro_metrics(betas, prefix, suffix))
        metrics.update(self.compute_weighted_metrics(betas, prefix, suffix))
        return metrics

    def compute_metrics(
        self,
        betas: Sequence[float] = (1,),
        prefix: str = "",
        suffix: str = "",
    ) -> dict[str, float | Tensor]:
        r"""Compute all the metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            All the metrics.

        Raises:
            EmptyTrackerError: if the confusion matrix is empty.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_predictions(
        ...     prediction=torch.tensor([0, 1, 2, 0, 0, 1]),
        ...     target=torch.tensor([2, 2, 2, 0, 0, 0]),
        ... )
        >>> confmat.compute_metrics()
        {'accuracy': 0.5,
         'balanced_accuracy': 0.333333...,
         'count': 6,
         'macro_precision': 0.555555...,
         'macro_recall': 0.333333...,
         'macro_f1_score': 0.388888...,
         'micro_precision': 0.5,
         'micro_recall': 0.5,
         'micro_f1_score': 0.5,
         'weighted_precision': 0.833333...,
         'weighted_recall': 0.5,
         'weighted_f1_score': 0.583333...,
         'precision': tensor([0.6667, 0.0000, 1.0000]),
         'recall': tensor([0.6667, 0.0000, 0.3333]),
         'f1_score': tensor([0.6667, 0.0000, 0.5000])}

        ```
        """
        return self.compute_scalar_metrics(
            betas=betas, prefix=prefix, suffix=suffix
        ) | self.compute_per_class_metrics(betas=betas, prefix=prefix, suffix=suffix)

    def get_records(
        self, betas: Sequence[float] = (1,), prefix: str = "", suffix: str = ""
    ) -> tuple[BaseRecord, ...]:
        r"""Get the records associated the metrics.

        Args:
            betas: The betas used to compute the f-beta score.
            prefix: The prefix for all the metrics.
            suffix: The suffix for all the metrics.

        Returns:
            The records for the metrics that are easily comparable.

        Example usage:

        ```pycon

        >>> from karbonn.utils.tracker import MulticlassConfusionMatrixTracker
        >>> confmat = MulticlassConfusionMatrixTracker.from_num_classes(5)
        >>> confmat.get_records()
        (MaxScalarRecord(name=accuracy, max_size=10, size=0),
         MaxScalarRecord(name=balanced_accuracy, max_size=10, size=0),
         MaxScalarRecord(name=macro_precision, max_size=10, size=0),
         MaxScalarRecord(name=macro_recall, max_size=10, size=0),
         MaxScalarRecord(name=micro_precision, max_size=10, size=0),
         MaxScalarRecord(name=micro_recall, max_size=10, size=0),
         MaxScalarRecord(name=weighted_precision, max_size=10, size=0),
         MaxScalarRecord(name=weighted_recall, max_size=10, size=0),
         MaxScalarRecord(name=macro_f1_score, max_size=10, size=0),
         MaxScalarRecord(name=micro_f1_score, max_size=10, size=0),
         MaxScalarRecord(name=weighted_f1_score, max_size=10, size=0))

        ```
        """
        trackers = [
            MaxScalarRecord(name=f"{prefix}accuracy{suffix}"),
            MaxScalarRecord(name=f"{prefix}balanced_accuracy{suffix}"),
            MaxScalarRecord(name=f"{prefix}macro_precision{suffix}"),
            MaxScalarRecord(name=f"{prefix}macro_recall{suffix}"),
            MaxScalarRecord(name=f"{prefix}micro_precision{suffix}"),
            MaxScalarRecord(name=f"{prefix}micro_recall{suffix}"),
            MaxScalarRecord(name=f"{prefix}weighted_precision{suffix}"),
            MaxScalarRecord(name=f"{prefix}weighted_recall{suffix}"),
        ]
        for beta in betas:
            trackers.extend(
                (
                    MaxScalarRecord(name=f"{prefix}macro_f{beta}_score{suffix}"),
                    MaxScalarRecord(name=f"{prefix}micro_f{beta}_score{suffix}"),
                    MaxScalarRecord(name=f"{prefix}weighted_f{beta}_score{suffix}"),
                )
            )
        return tuple(trackers)


def check_confusion_matrix(matrix: Tensor) -> None:
    r"""Check if the input matrix is a valid confusion matrix.

    Args:
        matrix: The confusion matrix to check.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.tracker.confmat import check_confusion_matrix
    >>> check_confusion_matrix(torch.zeros(3, 3, dtype=torch.long))

    ```
    """
    if matrix.ndim != 2:
        msg = (
            "Incorrect matrix dimensions. The matrix must have 2 dimensions but "
            f"received {matrix.ndim} dimensions"
        )
        raise ValueError(msg)
    if matrix.shape[0] != matrix.shape[1]:
        msg = (
            "Incorrect matrix shape. The matrix must be a squared matrix but "
            f"received {matrix.shape}"
        )
        raise ValueError(msg)
    if matrix.dtype != torch.long:
        msg = (
            "Incorrect matrix data type. The matrix data type must be long but "
            f"received {matrix.dtype}"
        )
        raise ValueError(msg)
    if not torch.all(matrix >= 0):
        msg = (
            "Incorrect matrix values. The matrix values must be greater or equal to 0 but "
            f"received:\n{matrix}"
        )
        raise ValueError(msg)


def check_op_compatibility_binary(
    current: BinaryConfusionMatrixTracker, other: BinaryConfusionMatrixTracker, op_name: str
) -> None:
    r"""Check if the confusion matrices for binary labels are compatible.

    Args:
        current: The current confusion matrix for binary labels.
        other: The other confusion matrix for binary labels.
        op_name: The operation name.

    Raises:
        TypeError: if the other matrix type is not compatible.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker.confmat import (
    ...     BinaryConfusionMatrixTracker,
    ...     check_op_compatibility_binary,
    ... )
    >>> check_op_compatibility_binary(
    ...     BinaryConfusionMatrixTracker(), BinaryConfusionMatrixTracker(), op_name="add"
    ... )

    ```
    """
    if not isinstance(other, BinaryConfusionMatrixTracker):
        msg = (
            f"Incorrect type {type(other)}. No implementation available to `{op_name}` "
            f"{type(current)} with {type(other)}"
        )
        raise TypeError(msg)


def check_op_compatibility_multiclass(
    current: MulticlassConfusionMatrixTracker, other: MulticlassConfusionMatrixTracker, op_name: str
) -> None:
    r"""Check if the confusion matrices for multiclass labels are
    compatible.

    Args:
        current: The current confusion matrix for multiclass labels.
        other: The other confusion matrix for multiclass labels.
        op_name: The operation name.

    Raises:
        TypeError: if the other matrix type is not compatible.
        ValueError: if the matrix shapes are different.

    Example usage:

    ```pycon

    >>> from karbonn.utils.tracker.confmat import (
    ...     MulticlassConfusionMatrixTracker,
    ...     check_op_compatibility_multiclass,
    ... )
    >>> check_op_compatibility_multiclass(
    ...     MulticlassConfusionMatrixTracker.from_num_classes(5),
    ...     MulticlassConfusionMatrixTracker.from_num_classes(5),
    ...     op_name="add",
    ... )

    ```
    """
    if not isinstance(other, MulticlassConfusionMatrixTracker):
        msg = (
            f"Incorrect type: {type(other)}. No implementation available to `{op_name}` "
            f"{type(current)} with {type(other)}"
        )
        raise TypeError(msg)
    if current.matrix.shape != other.matrix.shape:
        msg = f"Incorrect shape: received {other.matrix.shape} but expect {current.matrix.shape}"
        raise ValueError(msg)


def str_binary_confusion_matrix(confmat: Tensor) -> str:
    r"""Return a string representation of the confusion matrix.

    Args:
        confmat: The binary confusion matrix.

    Returns:
        A string representation of the confusion matrix.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.utils.tracker.confmat import str_binary_confusion_matrix
    >>> print(str_binary_confusion_matrix(torch.tensor([[1001, 42], [123, 789]])))
    ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                     ┃ predicted negative (0) ┃ predicted positive (1) ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual negative (0) ┃ [TN]  1,001            ┃ [FP]  42               ┃
    ┣━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ actual positive (1) ┃ [FN]  123              ┃ [TP]  789              ┃
    ┗━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛

    ```
    """
    if confmat.shape != (2, 2):
        msg = f"Expected a 2x2 confusion matrix but received: {confmat.shape}"
        raise RuntimeError(msg)
    confmat = confmat.long()
    table = [
        ["", "predicted negative (0)", "predicted positive (1)"],
        ["actual negative (0)", f"[TN]  {confmat[0, 0]:,}", f"[FP]  {confmat[0, 1]:,}"],
        ["actual positive (1)", f"[FN]  {confmat[1, 0]:,}", f"[TP]  {confmat[1, 1]:,}"],
    ]
    return str_table(table, tablefmt="heavy_grid")
