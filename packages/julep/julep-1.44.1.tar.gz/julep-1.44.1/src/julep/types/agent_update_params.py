# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import TypedDict

__all__ = ["AgentUpdateParams", "DefaultSettings"]


class AgentUpdateParams(TypedDict, total=False):
    about: str

    default_settings: Optional[DefaultSettings]
    """Default settings for the chat session (also used by the agent)"""

    instructions: Union[str, List[str]]

    metadata: Optional[object]

    model: str

    name: str


class DefaultSettings(TypedDict, total=False):
    frequency_penalty: Optional[float]

    length_penalty: Optional[float]

    min_p: Optional[float]

    presence_penalty: Optional[float]

    repetition_penalty: Optional[float]

    temperature: Optional[float]

    top_p: Optional[float]
