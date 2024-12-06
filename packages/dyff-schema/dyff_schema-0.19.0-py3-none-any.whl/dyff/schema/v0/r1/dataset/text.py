# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import pydantic

from ..base import DyffSchemaBaseModel, Int64


class TaggedSpan(DyffSchemaBaseModel):
    """A contiguous subsequence of text with a corresponding tag."""

    start: Int64 = pydantic.Field(
        description="The index of the first character in the span"
    )
    end: Int64 = pydantic.Field(
        description="The index one past the final character in the span"
    )
    tag: str = pydantic.Field(description="The tag of the span")


class TaggedSpans(DyffSchemaBaseModel):
    """A list of tagged spans."""

    spans: list[TaggedSpan] = pydantic.Field(description="A list of tagged spans")


class Text(DyffSchemaBaseModel):
    """Text data."""

    text: str = pydantic.Field(description="Text data")


class Tokens(DyffSchemaBaseModel):
    """A list of text tokens."""

    tokens: list[str] = pydantic.Field(
        default_factory=list, description="A list of text tokens"
    )
