# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FactcheckCreateParams"]


class FactcheckCreateParams(TypedDict, total=False):
    claim: Required[str]
    """The claim to be fact-checked."""

    context: Required[str]
    """The context to fact-check against."""
