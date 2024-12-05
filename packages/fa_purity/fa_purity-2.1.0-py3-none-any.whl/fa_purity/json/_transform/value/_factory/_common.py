from __future__ import (
    annotations,
)

from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity._core.result import (
    Result,
    ResultE,
)
from fa_purity._core.utils import (
    cast_exception,
    raise_exception,
)
from fa_purity.json._core.primitive import (
    Primitive,
)
from fa_purity.json._core.value import (
    JsonObj,
    JsonValue,
)
from fa_purity.json._transform.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


class HandledException(Exception):
    pass


def from_list(
    raw: Union[List[Primitive], FrozenList[Primitive]]
) -> FrozenList[JsonValue]:
    return tuple(
        JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(item))
        for item in raw
    )


def from_dict(
    raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
) -> JsonObj:
    return FrozenDict(
        {
            key: JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(val))
            for key, val in raw.items()
        }
    )


def from_any(raw: Optional[_T]) -> ResultE[JsonValue]:
    if isinstance(raw, (FrozenDict, dict)):
        try:
            json_dict = FrozenDict(
                {
                    JsonPrimitiveFactory.from_any(key)
                    .bind(JsonPrimitiveUnfolder.to_str)
                    .alt(HandledException)
                    .alt(raise_exception)
                    .to_union(): from_any(val)
                    .alt(HandledException)
                    .alt(raise_exception)
                    .to_union()
                    for key, val in raw.items()
                }
            )
            return Result.success(JsonValue.from_json(json_dict))
        except HandledException as err:
            return Result.failure(cast_exception(err))
    if isinstance(raw, (list, tuple)):
        try:
            json_list = tuple(
                from_any(item)
                .alt(HandledException)
                .alt(raise_exception)
                .to_union()
                for item in raw
            )
            return Result.success(JsonValue.from_list(json_list))
        except HandledException as err:
            return Result.failure(cast_exception(err))
    return JsonPrimitiveFactory.from_any(raw).map(JsonValue.from_primitive)


def from_raw_dict(raw: Dict[str, Any]) -> ResultE[JsonObj]:  # type: ignore[misc]
    err = Result.failure(cast_exception(TypeError("Not a `JsonObj`")), JsonObj)
    return from_any(raw).bind(  # type: ignore[misc]
        lambda jv: jv.map(
            lambda _: err,
            lambda _: err,
            lambda x: Result.success(x),
        )
    )
