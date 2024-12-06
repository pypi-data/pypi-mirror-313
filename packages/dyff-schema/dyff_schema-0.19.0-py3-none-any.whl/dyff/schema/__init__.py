# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import importlib
from typing import Iterable, Type

import pydantic

from .base import DyffSchemaBaseModel
from .version import SomeSchemaVersion


def _symbol(fully_qualified_name):
    tokens = fully_qualified_name.split(".")
    module_name = ".".join(tokens[:-1])
    member = tokens[-1]
    module = importlib.import_module(module_name)
    return getattr(module, member)


def product_schema(
    schemas: Iterable[Type[DyffSchemaBaseModel]],
) -> Type[DyffSchemaBaseModel]:
    return pydantic.create_model("Product", __base__=tuple(schemas))


# TODO: Should have a way of registering schema names rather than allowing
# arbitrary imports.
def named_data_schema(
    name: str, schema_version: SomeSchemaVersion
) -> Type[DyffSchemaBaseModel]:
    version, revision = schema_version.split(".")
    return _symbol(f"dyff.schema.v{version}.r{revision}.dataset.{name}")


__all__ = [
    "named_data_schema",
    "product_schema",
]
