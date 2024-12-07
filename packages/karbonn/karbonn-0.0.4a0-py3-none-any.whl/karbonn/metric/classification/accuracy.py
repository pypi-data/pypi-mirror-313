r"""Contain accuracy metrics."""

from __future__ import annotations

__all__ = ["Accuracy", "TopKAccuracy"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_mapping
from torch.nn import Identity, Module

from karbonn.metric import BaseMetric
from karbonn.metric.state import AccuracyState, BaseState, setup_state
from karbonn.metric.state_ import BaseStateMetric
from karbonn.utils import setup_module

if TYPE_CHECKING:
    from collections.abc import Sequence

    from minrecord import BaseRecord
    from torch import Tensor

logger = logging.getLogger(__name__)


class Accuracy(BaseStateMetric):
    r"""Implement a categorical accuracy metric.

    Args:
        state: The metric state or its configuration. If ``None``,
            ``AccuracyState`` is instantiated.
        transform: The transformation applied on the predictions to
            generate the predicted categorical labels. If ``None``, the
            identity module is used. The transform module must take
            a single input tensor and output a single tensor.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import Accuracy
    >>> metric = Accuracy()
    >>> metric
    Accuracy(
      (state): AccuracyState(
          (tracker): MeanTensorTracker(count=0, total=0.0)
          (track_count): True
        )
      (transform): Identity()
    )
    >>> metric(torch.tensor([1, 0]), torch.tensor([1, 0]))
    >>> metric.value()
    {'accuracy': 1.0, 'count': 2}
    >>> metric(torch.tensor([[0, 2]]), torch.tensor([1, 2]))
    >>> metric.value()
    {'accuracy': 0.75, 'count': 4}
    >>> metric.reset()
    >>> metric(torch.tensor([[1, 1]]), torch.tensor([1, 2]))
    >>> metric.value()
    {'accuracy': 0.5, 'count': 2}

    ```
    """

    def __init__(
        self,
        state: BaseState | dict | None = None,
        transform: Module | dict | None = None,
    ) -> None:
        super().__init__(state=state or AccuracyState())
        self.transform = setup_module(transform or Identity())

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the accuracy metric given a mini-batch of examples.

        Args:
            prediction: The predicted labels or the predictions.
                This input must be a ``torch.Tensor`` of  shape
                ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, num_classes)``
                and type long or float. If the input is the
                predictions/scores, then the ``transform`` module
                should be set to transform the predictions/scores
                to categorical labels where the values are in
                ``{0, 1, ..., num_classes-1}``.
            target: The categorical targets. The values have to be in
                ``{0, 1, ..., num_classes-1}``. This input must be a
                ``torch.Tensor`` of shape ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, 1)`` and type long or float.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import Accuracy
        >>> metric = Accuracy()
        >>> metric(torch.tensor([1, 2, 0, 1]), torch.tensor([1, 2, 0, 1]))
        >>> metric.value()
        {'accuracy': 1.0, 'count': 4}

        ```
        """
        prediction = self.transform(prediction)
        self._state.update(prediction.eq(target.view_as(prediction)))


class TopKAccuracy(BaseMetric):
    r"""Implement the accuracy at k metric a.k.a. top-k accuracy.

    Args:
        topk: The k values used to evaluate the top-k accuracy metric.

    Example usage:

    ```pycon

    >>> import torch
    >>> from karbonn.metric import TopKAccuracy
    >>> metric = TopKAccuracy(topk=(1,))
    >>> metric
    TopKAccuracy(
      (topk): (1,)
      (states):
        (1): AccuracyState(
              (tracker): MeanTensorTracker(count=0, total=0.0)
              (track_count): True
            )
    )
    >>> metric(torch.tensor([[0.0, 2.0, 1.0], [2.0, 1.0, 0.0]]), torch.tensor([1, 0]))
    >>> metric.value()
    {'top_1_accuracy': 1.0, 'top_1_count': 2}
    >>> metric(torch.tensor([[0.0, 2.0, 1.0], [2.0, 1.0, 0.0]]), torch.tensor([1, 2]))
    >>> metric.value()
    {'top_1_accuracy': 0.75, 'top_1_count': 4}
    >>> metric.reset()
    >>> metric(torch.tensor([[0.0, 2.0, 1.0], [2.0, 1.0, 0.0]]), torch.tensor([1, 2]))
    >>> metric.value("acc_")
    {'acc_top_1_accuracy': 0.5, 'acc_top_1_count': 2}

    ```
    """

    def __init__(self, topk: Sequence[int] = (1, 5), state: BaseState | dict | None = None) -> None:
        super().__init__()
        self._topk = topk if isinstance(topk, tuple) else tuple(topk)
        self._maxk = max(self._topk)

        state = setup_state(state or AccuracyState())
        self._states = {tol: state.clone() for tol in self._topk}

    def extra_repr(self) -> str:
        return repr_mapping(
            {
                "topk": self._topk,
                "states": "\n" + repr_indent(repr_mapping(self._states)),
            }
        )

    @property
    def topk(self) -> tuple[int, ...]:
        return self._topk

    def forward(self, prediction: Tensor, target: Tensor) -> None:
        r"""Update the accuracy metric given a mini-batch of examples.

        Args:
            prediction: The predicted labels as a ``torch.Tensor`` of
                shape ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, num_classes)``
                and type long or float.
            target: The categorical targets. The values have to be in
                ``{0, 1, ..., num_classes-1}``. This input must be a
                ``torch.Tensor`` of shape ``(d0, d1, ..., dn)`` or
                ``(d0, d1, ..., dn, 1)`` and type long or float.

        Example usage:

        ```pycon

        >>> import torch
        >>> from karbonn.metric import TopKAccuracy
        >>> metric = TopKAccuracy(topk=(1,))
        >>> metric(torch.tensor([[0.0, 2.0, 1.0], [2.0, 1.0, 0.0]]), torch.tensor([1, 0]))
        >>> metric.value()
        {'top_1_accuracy': 1.0, 'top_1_count': 2}

        ```
        """
        pred = prediction.topk(self._maxk, -1, True, True)[1]
        correct = pred.eq(target.view(*pred.shape[:-1], 1).expand_as(pred)).float()
        for k, state in self._states.items():
            state.update(correct[..., :k].sum(dim=-1))

    def get_records(self, prefix: str = "", suffix: str = "") -> tuple[BaseRecord, ...]:
        records = []
        for k, state in self._states.items():
            records.extend(state.get_records(prefix=f"{prefix}top_{k}_", suffix=suffix))
        return tuple(records)

    def reset(self) -> None:
        for state in self._states.values():
            state.reset()

    def value(self, prefix: str = "", suffix: str = "") -> dict:
        results = {}
        for k, state in self._states.items():
            results.update(state.value(prefix=f"{prefix}top_{k}_", suffix=suffix))
        return results
