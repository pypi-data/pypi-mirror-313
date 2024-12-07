r"""Define the tracker specific exceptions."""

from __future__ import annotations

__all__ = ["EmptyTrackerError"]


class EmptyTrackerError(Exception):
    r"""Raised if the tracker is empty because it is not possible to
    evaluate an empty tracker."""
