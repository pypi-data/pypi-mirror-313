# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
from __future__ import annotations

import functools
import json
from typing import Any, Iterable, NamedTuple, Protocol, Type

import jsonpath_ng as jsonpath
from jsonpath_ng.exceptions import JSONPathError

from dyff.schema.platform import SchemaAdapter


def map_structure(fn, data):
    """Given a JSON data structure ``data``, create a new data structure instance with
    the same shape as ``data`` by applying ``fn`` to each "leaf" value in the nested
    data structure."""
    if isinstance(data, dict):
        return {k: map_structure(fn, v) for k, v in data.items()}
    elif isinstance(data, list):
        return [map_structure(fn, x) for x in data]
    else:
        return fn(data)


def flatten_object(
    obj: dict, *, max_depth: int | None = None, add_prefix: bool = True
) -> dict:
    """Flatten a JSON object the by creating a new object with a key for each "leaf"
    value in the input. If ``add_prefix`` is True, the key will be equal to the "path"
    string of the leaf, i.e., "obj.field.subfield"; otherwise, it will be just
    "subfield".

    Nested lists are considered "leaf" values, even if they contain objects.
    """

    def impl(obj, flat, max_depth, prefix=None):
        if prefix is None:
            prefix = []
        depth_limit = (max_depth is not None) and (max_depth < len(prefix))
        if not depth_limit and isinstance(obj, dict):
            for k, v in obj.items():
                impl(v, flat, max_depth, prefix=(prefix + [k]))
        else:
            if add_prefix:
                flat[".".join(prefix)] = obj
            else:
                flat[prefix[-1]] = obj

    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    flat: dict[str, Any] = {}
    impl(obj, flat, max_depth)
    return flat


class HTTPData(NamedTuple):
    content_type: str
    data: Any


class Adapter(Protocol):
    """Transforms streams of JSON structures."""

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        raise NotImplementedError()


class TransformJSON:
    """Transform an input JSON structure by creating a new output JSON structure where
    all of the "leaf" values are populated by either:

        1. A provided JSON literal value, or
        2. The result of a jsonpath query on the input structure.

    For example, if the ``output_structure`` parameter is::

        {
            "id": "$.object.id",
            "name": "literal",
            "children": {"left": "$.list[0]", "right": "$.list[1]"}
        }

    and the data is::

        {
            "object": {"id": 42, "name": "spam"},
            "list": [1, 2]
        }

    Then applying the transformer to the data will result in the new structure::

        {
            "id": 42,
            "name": "literal",
            "children: {"left": 1, "right": 2}
        }

    A value is interpreted as a jsonpath query if it is a string that starts
    with the '$' character. If you need a literal string that starts with
    the '$' character, escape it with a second '$', e.g., "$$PATH" will appear
    as the literal string "$PATH" in the output.

    All of the jsonpath queries must return *exactly one value* when executed
    against each input item. If not, a ``ValueError`` will be raised.
    """

    def __init__(self, configuration: dict):
        """
        Parameters:
            ``output_structure``: A JSON object where all the "leaf" values
                are strings containing jsonpath queries.
        """
        if configuration != json.loads(json.dumps(configuration)):
            raise ValueError("configuration is not valid JSON")
        self.output_structure = configuration
        try:
            self._expressions = map_structure(
                self._jsonpath_expr_or_literal, self.output_structure
            )
        except JSONPathError as ex:
            raise ValueError(
                "output_structure leaf values must be JSON literals or jsonpath query strings"
            ) from ex

    def _jsonpath_expr_or_literal(self, x):
        if isinstance(x, str):
            if x.startswith("$"):
                if x.startswith("$$"):
                    # Literal string -- remove "escape" character
                    return x[1:]
                else:
                    return jsonpath.parse(x)
        return x

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        def query(data, expr):
            if not isinstance(expr, jsonpath.JSONPath):
                # Literal
                return expr
            results = expr.find(data)
            if len(results) == 0:
                raise ValueError(f"no match for {expr}")
            elif len(results) > 1:
                raise ValueError(f"multiple results for {expr}")
            return results[0].value

        for item in stream:
            transformed = map_structure(
                lambda expr: query(item, expr), self._expressions
            )
            yield transformed


class EmbedIndex:
    """Adds one or more fields to each member of the specified collections that
    represent "indexes", or possible sort orders, for the collections.

    For example, if the input data is::

        {
            "choices": [{"label": "foo"}, {"label": "bar"}],
            "ranks": [1, 0]
        }

    And the configuration is::

        {
            "collections": ["choices"],
            "index": {
                "outputOrder": None,
                "rankOrder": "$.ranks[*]"
            }
        }

    Then the output will be::

        {
            "collections": [
                {"label": "foo", "outputOrder": 0, "rankOrder": 1},
                {"label": "bar", "outputOrder": 1, "rankOrder": 0}
            ],
            "ranks": [1, 0]
        }

    The "collections" part of the configuration is a list of collections to
    embed the indexes into. They must all have the same length, and their
    elements must be JSON Objects (that is, dicts).

    The "index" part of the configuration is a mapping from new field names to
    expressions for generating the index. If the expression is None, then
    the field will be populated with the index of the element in the
    collection. If the expression is not None, it must be a JSONPath query
    that returns a *list* of the same length as the collection.
    """

    def __init__(self, configuration: dict):
        self.collections = configuration["collections"]
        self.index = configuration.get("index", {})
        self._index_expr = {k: v and jsonpath.parse(v) for k, v in self.index.items()}

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            length = None
            for k in self.collections:
                collection_length = len(item[k])
                if length is None:
                    length = collection_length
                elif length != collection_length:
                    raise ValueError()
            assert length is not None

            item = item.copy()
            for index_name, index_source in self.index.items():
                if index_source is None:
                    index = list(range(length))
                else:
                    result = self._index_expr[index_name].find(item)
                    index = [match.value for match in result]
                for k in self.collections:
                    collection_items = [ci.copy() for ci in item[k]]
                    for i, d in zip(index, collection_items):
                        d[index_name] = i
                    item[k] = collection_items

            yield item


class ExplodeCollections:
    """Explodes one or more top-level lists of the same length into multiple records,
    where each record contains the corresponding value from each list. This is useful
    for turning nested-list representations into "relational" representations where the
    lists are converted to multiple rows with a unique index.

    The ``configuration`` argument is a dictionary::

        {
            "collections": list[str],
            "index": dict[str, str | None]
        }

    For example, if the input data is::

        [
            {"numbers": [1, 2, 3], "squares": [1, 4, 9], "scalar": "foo"},
            {"numbers": [4, 5], "squares": [16, 25], "scalar": bar"}
        ]

    Then ``ExplodeCollections({"collections": ["numbers", "squares"]})`` will
    yield this output data::

        [
            {"numbers": 1, "squares": 1, "scalar": "foo"},
            {"numbers": 2, "squares": 4, "scalar": "foo"},
            {"numbers": 3, "squares": 9, "scalar": "foo"},
            {"numbers": 4, "squares": 16, "scalar": "bar"},
            {"numbers": 5, "squares": 25, "scalar": "bar"},
        ]

    You can also create *indexes* for the exploded records. Given the following
    configuration::

        {
            "collections": ["choices"],
            "index": {
                "collection/index": None,
                "collection/rank": "$.choices[*].meta.rank"
            }
        }

    then for the input::

        [
            {
                "choices": [
                    {"label": "foo", "meta": {"rank": 1}},
                    {"label": "bar", "meta": {"rank": 0}}
                ]
            },
            ...
        ]

     the output will be::

        [
            {
                "choices": {"label": "foo", "meta": {"rank": 1}},
                "collection/index": 0,
                "collection/rank": 1
            },
            {
                "choices": {"label": "bar", "meta": {"rank": 0}},
                "collection/index": 1,
                "collection/rank": 0
            },
            ...
        ]

    The ``None`` value for the ``"collection/index"`` index key means that the
    adapter should assign indices from ``0...n-1`` automatically. If the value
    is not ``None``, it must be a JSONPath query to execute against the
    *pre-transformation* data that returns a *list*. Notice how the example
    uses ``$.choices[*]`` to get the *list* of choices.
    """

    def __init__(self, configuration: dict):
        self.collections = configuration["collections"]
        self.index = configuration.get("index", {})
        self._index_expr = {k: v and jsonpath.parse(v) for k, v in self.index.items()}

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            collections = {k: item[k] for k in self.collections}
            other = {k: v for k, v in item.items() if k not in self.collections}

            length = None
            for c in collections.values():
                if length is not None and length != len(c):
                    raise ValueError()
                length = len(c)
            assert length is not None

            for index_name, index_source in self.index.items():
                if index_source is None:
                    collections[index_name] = range(length)
                else:
                    result = self._index_expr[index_name].find(item)
                    matches = [match.value for match in result]
                    collections[index_name] = matches

            for t in zip(*collections.values()):
                transformed = other.copy()
                transformed.update({k: t[i] for i, k in enumerate(collections)})
                yield transformed


class FlattenHierarchy:
    """Flatten a JSON object -- or the JSON sub-objects in named fields -- by creating a
    new object with a key for each "leaf" value in the input.

    The ``configuration`` options are::

        {
            "fields": list[str],
            "depth": int | None,
            "addPrefix": bool
        }

    If ``fields`` is missing or empty, the flattening is applied to the root
    object. The ``depth`` option is the maximum recursion depth. If
    ``addPrefix`` is True (the default), then the resultint fields will be
    named like ``"path.to.leaf"`` to avoid name conflicts.

    For example, if the configuration is::

        {
            "fields": ["choices"],
            "depth": 1,
            "addPrefix": True
        }

    and the input is::

        {
            "choices": {"label": "foo", "metadata": {"value": 42}},
            "scores": {"top1": 0.9}
        }

    then the output will be::

        {
            "choices.label": "foo",
            "choices.metadata": {"value": 42},
            "scores": {"top1": 0.9}
        }

    Note that nested lists are considered "leaf" values, even if they contain
    objects.
    """

    def __init__(self, configuration=None):
        self.fields = configuration and configuration.get("fields")
        self.depth = configuration and configuration.get("depth")
        self.addPrefix = (configuration is None) or configuration.get("addPrefix")

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            if self.fields:
                item = item.copy()
                for f in self.fields:
                    field = item.pop(f)
                    flat = flatten_object(
                        {f: field}, max_depth=self.depth, add_prefix=self.addPrefix
                    )
                    item.update(flat)
                yield item
            else:
                yield flatten_object(
                    item, max_depth=self.depth, add_prefix=self.addPrefix
                )


class Rename:
    """Rename top-level fields in each JSON object.

    The input is a dictionary ``{old_name: new_name}``.
    """

    def __init__(self, configuration: dict):
        self.names_mapping = configuration

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            renamed = item.copy()
            for old, new in self.names_mapping.items():
                old_value = renamed.pop(old)
                renamed[new] = old_value
            yield renamed


class Drop:
    """Drop named top-level fields.

    The configuration is a dictionary::

        {
            "fields": list[str]
        }
    """

    def __init__(self, configuration: dict):
        self.fields = configuration["fields"]

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            retained: dict = item.copy()
            for field in self.fields:
                retained.pop(field, None)
            yield retained


class Select:
    """Select named top-level fields and drop the others.

    The configuration is a dictionary::

        {
            "fields": list[str]
        }
    """

    def __init__(self, configuration: dict):
        self.fields = configuration["fields"]

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            yield {field: item[field] for field in self.fields}


class Map:
    """For each input item, map another Adapter over the elements of each of the named
    nested collections within that item.

    The configuration is a dictionary::

        {
            "collections": list[str],
            "adapter": {
                "kind": <AdapterType>
                "configuration": <AdapterConfigurationDictionary>
            }
        }
    """

    def __init__(self, configuration: dict):
        self.collections = configuration["collections"]
        self.adapter = create_adapter(configuration["adapter"])

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        for item in stream:
            item = item.copy()
            for c in self.collections:
                collection = item[c]
                transformed = list(self.adapter(collection))
                item[c] = transformed
            yield item


class Pipeline:
    """Apply multiple adapters in sequence."""

    def __init__(self, adapters: list[Adapter]):
        self._adapters = list(adapters)

    def _impl(self, index: int, stream: Iterable[dict]) -> Iterable[dict]:
        # FIXME: Recursion depth could become an issue for very long pipelines
        if index < 0:
            yield from stream
        else:
            yield from self._adapters[index](self._impl(index - 1, stream))

    def __call__(self, stream: Iterable[dict]) -> Iterable[dict]:
        yield from self._impl(len(self._adapters) - 1, stream)


@functools.lru_cache()
def known_adapters() -> dict[str, Type[Adapter]]:
    return {
        t.__name__: t
        for t in [
            Drop,
            ExplodeCollections,
            FlattenHierarchy,
            Map,
            Pipeline,
            Rename,
            Select,
            TransformJSON,
        ]
    }


def create_adapter(adapter_spec: SchemaAdapter | dict) -> Adapter:
    if isinstance(adapter_spec, SchemaAdapter):
        adapter_spec = adapter_spec.dict()
    kind = adapter_spec["kind"]
    if (adapter_t := known_adapters().get(kind)) is not None:
        adapter_config = adapter_spec.get("configuration")
        args = []
        if adapter_config is not None:
            args.append(adapter_config)
        return adapter_t(*args)
    else:
        raise ValueError(f"unknown adapter kind {kind}")


def create_pipeline(adapter_specs: Iterable[SchemaAdapter | dict]) -> Pipeline:
    return Pipeline([create_adapter(spec) for spec in adapter_specs])


__all__ = [
    "Adapter",
    "HTTPData",
    "Pipeline",
    "create_adapter",
    "create_pipeline",
    "flatten_object",
    "known_adapters",
    "map_structure",
    *known_adapters().keys(),
]


def _test():
    data = {
        "object": {"foo": "bar"},
        "list": [{"value": 1}, {"value": 2}, {"value": 3}],
        "string": "foobar",
        "number": 42,
        "null": None,
    }

    transformer = TransformJSON(
        {"object_copy": "$.object", "list_copy": "$.list", "scalar_copy": "$.string"}
    )
    print(list(transformer([data])))

    transformer = TransformJSON({"nested": "$.object.foo"})
    print(list(transformer([data])))

    transformer = TransformJSON(
        {"id": "$.object.id", "children": {"left": "$.list[0]", "right": "$.list[1]"}}
    )
    print(
        list(
            transformer(
                [
                    {"object": {"id": 42, "name": "spam"}, "list": [1, 2]},
                ]
            )
        )
    )

    data = {
        "someField": 42,
        "choices": [
            {
                "label": "foo",
                "meta": {
                    "index": 0,
                },
            },
            {
                "label": "bar",
                "meta": {
                    "index": 1,
                },
            },
        ],
        "ranks": [1, 0],
    }

    transformer = Pipeline(
        [
            # ExplodeCollections(
            #     {
            #         "collections": ["choices", "ranks"],
            #         "index": {
            #         #     "collection/rank": "$.ranks[*]",
            #         #     "collection/sample": "$.choices[*].meta.index",
            #             "collection/index": None,
            #         }
            #     }
            # ),
            # FlattenHierarchy(),
            EmbedIndex(
                {
                    "collections": ["choices"],
                    "index": {
                        # "index/rank": "$.ranks[*]",
                        "index/rank": None
                    },
                }
            ),
            # Map(
            #     ["choices"],
            #     TransformJSON(
            #         {
            #             "label": "$.label",
            #             "index/rank": "$['index/rank']"
            #         }
            #     )
            # )
            create_adapter(
                {
                    "kind": "Map",
                    "configuration": {
                        "collections": ["choices"],
                        "adapter": {
                            "kind": "Select",
                            "configuration": {
                                "fields": ["label", "index/rank"],
                            },
                        },
                    },
                }
            ),
            Rename({"choices": "responses"}),
            # Select([
            #     "collection/index",
            #     "collection/rank",
            #     "label"
            # ])
            # TransformJSON(
            #     {
            #         "label": "$.choices.label",
            #         "collection/rank": "$.'collection/rank'",
            #         "collection/index": "$.'collection/index'"
            #     }
            # ),
            Drop({"fields": ["ranks", "someField"]}),
            # Select(["label", "collection/rank", "collection/index"])
            Map(
                {
                    "collections": ["responses"],
                    "adapter": {
                        "kind": "TransformJSON",
                        "configuration": {
                            "truth": "$.label",
                            "consequences": 42,
                            "envvar": "$$PATH",
                            "details": {"foo": "bar"},
                        },
                    },
                }
            ),
        ]
    )
    transformed = list(transformer([data]))
    print(transformed)

    # print(pandas.json_normalize([item.data for item in transformed]))

    # transformer = TransformJSON({"multiple": "$.list[*].value"})
    # print(list(transformer([data])))

    print("=====")
    print([data])
    transformer = Pipeline(
        [
            ExplodeCollections(
                {
                    "collections": ["choices", "ranks"],
                    "index": {
                        "collection/rank": "$.ranks[*]",
                        #     "collection/sample": "$.choices[*].meta.index",
                        "collection/index": None,
                    },
                }
            ),
            FlattenHierarchy({"addPrefix": True}),
        ]
    )
    transformed = list(transformer([data]))
    print("-----")
    print(transformed)

    data = {
        "_index_": 42,
        "text": [
            "it was the worst of times",
            "it was the blurst of times",
        ],
    }

    transformer = Pipeline(
        [
            ExplodeCollections(
                {"collections": ["text"], "index": {"_response_index_": None}}
            )
        ]
    )

    print("=====")
    print([data])
    transformed = list(transformer([data]))
    print("-----")
    print(transformed)

    data = {
        "covariate": 42,
        "responses": [
            {"text": "it was the worst of times"},
            {"text": "it was the blurst of times"},
        ],
    }

    transformer = Pipeline(
        [
            ExplodeCollections({"collections": ["responses"]}),
            FlattenHierarchy({"addPrefix": False}),
        ]
    )

    print("=====")
    print([data])
    transformed = list(transformer([data]))
    print("-----")
    print(transformed)

    create_pipeline(
        [
            # {"text": ["The answer"]} -> [{"text": "The answer"}]
            SchemaAdapter(
                kind="ExplodeCollections",
                configuration={"collections": ["text"]},
            ).dict()
        ]
    )


if __name__ == "__main__":
    _test()
