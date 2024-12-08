# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "ChatSettings",
    "ResponseFormat",
    "ResponseFormatSimpleCompletionResponseFormat",
    "ResponseFormatSchemaCompletionResponseFormat",
]


class ResponseFormatSimpleCompletionResponseFormat(BaseModel):
    type: Optional[Literal["text", "json_object"]] = None


class ResponseFormatSchemaCompletionResponseFormat(BaseModel):
    json_schema: object

    type: Optional[Literal["json_schema"]] = None


ResponseFormat: TypeAlias = Union[
    ResponseFormatSimpleCompletionResponseFormat, ResponseFormatSchemaCompletionResponseFormat, None
]


class ChatSettings(BaseModel):
    agent: Optional[str] = None

    frequency_penalty: Optional[float] = None

    length_penalty: Optional[float] = None

    logit_bias: Optional[Dict[str, float]] = None

    max_tokens: Optional[int] = None

    min_p: Optional[float] = None

    model: Optional[str] = None

    presence_penalty: Optional[float] = None

    repetition_penalty: Optional[float] = None

    response_format: Optional[ResponseFormat] = None

    seed: Optional[int] = None

    stop: Optional[List[str]] = None

    stream: Optional[bool] = None

    temperature: Optional[float] = None

    top_p: Optional[float] = None
