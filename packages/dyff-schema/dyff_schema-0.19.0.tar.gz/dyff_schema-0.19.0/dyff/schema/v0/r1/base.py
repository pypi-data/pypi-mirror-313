# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Generic, Literal, NamedTuple, Optional, Type, TypeVar

import pydantic

# ----------------------------------------------------------------------------
# Fixed-width numeric type value bounds


class _dtype(NamedTuple):
    float32: str = "float32"
    float64: str = "float64"
    int8: str = "int8"
    int16: str = "int16"
    int32: str = "int32"
    int64: str = "int64"
    uint8: str = "uint8"
    uint16: str = "uint16"
    uint32: str = "uint32"
    uint64: str = "uint64"


DTYPE = _dtype()


def float32_max() -> float:
    return 3.4028235e38


def float64_max() -> float:
    return 1.7976931348623157e308


def int8_max() -> int:
    return 127


def int8_min() -> int:
    return -128


def int16_max() -> int:
    return 32767


def int16_min() -> int:
    return -32768


def int32_max() -> int:
    return 2147483647


def int32_min() -> int:
    return -2147483648


def int64_max() -> int:
    return 9223372036854775807


def int64_min() -> int:
    return -9223372036854775808


def uint8_max() -> int:
    return 255


def uint8_min() -> int:
    return 0


def uint16_max() -> int:
    return 65535


def uint16_min() -> int:
    return 0


def uint32_max() -> int:
    return 4294967295


def uint32_min() -> int:
    return 0


def uint64_max() -> int:
    return 18446744073709551615


def uint64_min() -> int:
    return 0


# ----------------------------------------------------------------------------
# Type annotation classes


_NumT = TypeVar("_NumT")
_ConstrainedNumT = TypeVar("_ConstrainedNumT")


class FixedWidthNumberMeta(
    Generic[_NumT, _ConstrainedNumT], pydantic.types.ConstrainedNumberMeta
):
    dtype: str
    minval: _NumT
    maxval: _NumT

    def __new__(cls, name: str, bases: Any, dct: dict[str, Any]) -> _ConstrainedNumT:  # type: ignore
        ge = dct.get("ge")
        gt = dct.get("gt")
        le = dct.get("le")
        lt = dct.get("lt")
        # For integers, we could technically have e.g., ``lt = maxval + 1``,
        # but then the bound is not representable in the same type, so we don't
        # allow it
        if ge is not None and ge < cls.minval:
            raise ValueError(f"ge must be >= minval")
        if gt is not None and gt < cls.minval:
            raise ValueError(f"gt must be >= minval")
        if le is not None and le > cls.maxval:
            raise ValueError(f"le must be <= maxval")
        if lt is not None and lt > cls.maxval:
            raise ValueError(f"lt must be <= maxval")
        # Note that the ConstrainedNumberMeta superclass checks that only one
        # each of ge/gt and le/lt is defined
        if ge is None and gt is None:
            ge = cls.minval  # default
        if le is None and lt is None:
            le = cls.maxval  # default
        # pydantic convention seems to be not to add None properties here
        if ge is not None:
            dct["ge"] = ge
        if gt is not None:
            dct["gt"] = gt
        if le is not None:
            dct["le"] = le
        if lt is not None:
            dct["lt"] = lt
        return super().__new__(cls, name, bases, dct)  # type: ignore


class DType:
    """Base class for pydantic custom types that have an Arrow .dtype."""

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any],
    ) -> None:
        dtype = type(cls).dtype  # type: ignore
        if dtype is None:
            raise ValueError("subclasses must set cls.dtype")
        super().__modify_schema__(field_schema)  # type: ignore
        field_schema.update({"dyff.io/dtype": dtype})


# DType must come first
class FixedWidthInt(DType, pydantic.ConstrainedInt):
    pass


# DType must come first
class FixedWidthFloat(DType, pydantic.ConstrainedFloat):
    pass


class Float32Meta(FixedWidthNumberMeta[float, pydantic.ConstrainedFloat]):
    dtype: str = DTYPE.float32
    minval: float = -float32_max()
    maxval: float = float32_max()


class Float64Meta(FixedWidthNumberMeta[float, pydantic.ConstrainedFloat]):
    dtype: str = DTYPE.float64
    minval: float = -float64_max()
    maxval: float = float64_max()


class Float32(FixedWidthFloat, metaclass=Float32Meta):
    """A 32-bit float ("single precision")"""


class Float64(FixedWidthFloat, metaclass=Float64Meta):
    """A 64-bit float ("double precision")"""


class Int8Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.int8
    minval: int = int8_min()
    maxval: int = int8_max()


class Int16Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.int16
    minval: int = int16_min()
    maxval: int = int16_max()


class Int32Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.int32
    minval: int = int32_min()
    maxval: int = int32_max()


class Int64Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.int64
    minval: int = int64_min()
    maxval: int = int64_max()


class UInt8Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.uint8
    minval: int = uint8_min()
    maxval: int = uint8_max()


class UInt16Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.uint16
    minval: int = uint16_min()
    maxval: int = uint16_max()


class UInt32Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.uint32
    minval: int = uint32_min()
    maxval: int = uint32_max()


class UInt64Meta(FixedWidthNumberMeta[int, pydantic.ConstrainedInt]):
    dtype: str = DTYPE.uint64
    minval: int = uint64_min()
    maxval: int = uint64_max()


class Int8(FixedWidthInt, metaclass=Int8Meta):
    """An 8-bit integer."""


class Int16(FixedWidthInt, metaclass=Int16Meta):
    """A 16-bit integer."""


class Int32(FixedWidthInt, metaclass=Int32Meta):
    """A 32-bit integer."""


class Int64(FixedWidthInt, metaclass=Int64Meta):
    """A 64-bit integer."""


class UInt8(FixedWidthInt, metaclass=UInt8Meta):
    """An 8-bit unsigned integer."""


class UInt16(FixedWidthInt, metaclass=UInt16Meta):
    """A 16-bit unsigned integer."""


class UInt32(FixedWidthInt, metaclass=UInt32Meta):
    """A 32-bit unsigned integer."""


class UInt64(FixedWidthInt, metaclass=UInt64Meta):
    """A 64-bit unsigned integer."""


# ----------------------------------------------------------------------------
# Type annotation constructors


def float32(
    *,
    strict: bool = False,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    allow_inf_nan: Optional[bool] = None,
) -> Type[float]:
    """Return a type annotation for a float32 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: float32(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
    )
    return type("Float32Value", (Float32,), namespace)


def float64(
    *,
    strict: bool = False,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    allow_inf_nan: Optional[bool] = None,
) -> Type[float]:
    """Return a type annotation for a float64 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: float64(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(
        strict=strict,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
    )
    return type("Float64Value", (Float64,), namespace)


def int8(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for an int8 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: int8(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("Int8Value", (Int8,), namespace)


def int16(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for an int16 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: int16(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("Int16Value", (Int16,), namespace)


def int32(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for an int32 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: int32(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("Int32Value", (Int32,), namespace)


def int64(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for an int64 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: int64(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("Int64Value", (Int64,), namespace)


def uint8(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for a uint8 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: uint8(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("UInt8Value", (UInt8,), namespace)


def uint16(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for a uint16 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: uint16(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("UInt16Value", (UInt16,), namespace)


def uint32(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for a uint32 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: uint32(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("UInt32Value", (UInt32,), namespace)


def uint64(
    *,
    strict: bool = False,
    gt: Optional[int] = None,
    ge: Optional[int] = None,
    lt: Optional[int] = None,
    le: Optional[int] = None,
    multiple_of: Optional[int] = None,
) -> Type[int]:
    """Return a type annotation for a uint64 field in a pydantic model.

    Note that any keyword arguments *must* be specified here, even if they
    can also be specified in ``pydantic.Field()``. The corresponding keyword
    arguments in ``pydantic.Field()`` will have *no effect*.

    Usage::

        class M(pydantic.BaseModel):
            # Notice how "lt" is specified in the type annotation, not Field()
            x: uint64(lt=42) = pydantic.Field(description="some field")
    """
    namespace = dict(strict=strict, gt=gt, ge=ge, lt=lt, le=le, multiple_of=multiple_of)
    return type("UInt64Value", (UInt64,), namespace)


_ListElementT = TypeVar("_ListElementT")


def list_(
    item_type: Type[_ListElementT], *, list_size: Optional[int] = None
) -> Type[list]:
    if list_size is None:
        return pydantic.conlist(item_type)
    else:
        if list_size <= 0:
            raise ValueError(f"list_size {list_size} must be > 0")
        return pydantic.conlist(item_type, min_items=list_size, max_items=list_size)


# mypy gets confused because 'dict' is the name of a method in DyffBaseModel
_ModelAsDict = dict[str, Any]


class DyffBaseModel(pydantic.BaseModel):
    """This must be the base class for *all pydantic models* in the Dyff schema.

    Overrides serialization functions to serialize by alias, so that "round-trip"
    serialization is the default for fields with aliases. We prefer aliases because we
    can 1) use _underscore_names_ as reserved names in our data schema, and 2) allow
    Python reserved words like 'bytes' as field names.
    """

    class Config:
        extra = pydantic.Extra.forbid

    def dict(self, *, by_alias: bool = True, **kwargs) -> _ModelAsDict:
        return super().dict(by_alias=by_alias, **kwargs)

    def json(self, *, by_alias: bool = True, **kwargs) -> str:
        return super().json(by_alias=by_alias, **kwargs)

    def model_dump(
        self,
        *,
        mode: Literal["python", "json"] = "python",
        by_alias: bool = True,
        **kwargs,
    ) -> _ModelAsDict:
        """Encode the object as a dict containing only JSON datatypes.

        .. deprecated:: 0.8.0

            FIXME: This emulates a Pydantic 2 feature, but the mode="json"
            option can only be implemented in an inefficient way. Remove when
            we convert to Pydantic 2. See: DYFF-223
        """
        if mode == "python":
            return self.dict(by_alias=by_alias, **kwargs)
        else:
            return json.loads(self.json(by_alias=by_alias, **kwargs))


# Note: I *really* wanted to require datetimes to have timezones, like in
# DyffRequestDefaultValidators, but some existing objects in the Auth database
# don't have timezones set currently for historical reasons. It's actually
# better if all datetimes in the system are UTC, so that their JSON
# representations (i.e., isoformat strings) are well-ordered.
class DyffSchemaBaseModel(DyffBaseModel):
    """This should be the base class for *almost all* non-request models in the Dyff
    schema. Models that do not inherit from this class *must* still inherit from
    DyffBaseModel.

    Adds a root validator to ensure that all datetime fields are represented in the UTC
    timezone. This is necessary to avoid errors when comparing "naive" and "aware"
    datetimes. Using the UTC timezone everywhere ensures that JSON representations of
    datetimes are well-ordered.
    """

    @pydantic.root_validator
    def _ensure_datetime_timezone_utc(cls, values):
        update = {}
        for k, v in values.items():
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    update[k] = v.replace(tzinfo=timezone.utc)
                elif v.tzinfo != timezone.utc:
                    update[k] = v.astimezone(timezone.utc)
        values.update(update)
        return values


__all__ = [
    "DTYPE",
    "DType",
    "DyffBaseModel",
    "DyffSchemaBaseModel",
    "FixedWidthFloat",
    "FixedWidthInt",
    "Float32",
    "Float64",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "float32",
    "float32_max",
    "float64",
    "float64_max",
    "int8",
    "int8_max",
    "int8_min",
    "int16",
    "int16_max",
    "int16_min",
    "int32",
    "int32_max",
    "int32_min",
    "int64",
    "int64_max",
    "int64_min",
    "list_",
    "uint8",
    "uint8_max",
    "uint8_min",
    "uint16",
    "uint16_max",
    "uint16_min",
    "uint32",
    "uint32_max",
    "uint32_min",
    "uint64",
    "uint64_max",
    "uint64_min",
]
