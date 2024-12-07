# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["SessionPatchParams"]


class SessionPatchParams(TypedDict, total=False):
    auto_run_tools: bool

    context_overflow: Optional[Literal["truncate", "adaptive"]]

    metadata: Optional[object]

    render_templates: bool

    situation: str

    token_budget: Optional[int]
