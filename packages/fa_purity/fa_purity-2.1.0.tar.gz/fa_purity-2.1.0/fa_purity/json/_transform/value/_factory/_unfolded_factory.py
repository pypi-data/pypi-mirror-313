from . import (
    _common,
)
from ._jval_factory import (
    JsonValueFactory,
)
from dataclasses import (
    dataclass,
)
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity.json._core.primitive import (
    Primitive,
)
from fa_purity.json._core.value import (
    JsonObj,
    JsonValue,
    RawUnfoldedJsonValue,
)
from typing import (
    Any,
    Dict,
    IO,
    List,
    Union,
)


def _only_json_objs(value: JsonValue) -> ResultE[JsonObj]:
    _factory: ResultFactory[JsonObj, Exception] = ResultFactory()
    return value.map(
        lambda _: _factory.failure(
            ValueError("Expected `JsonObj` not `JsonPrimitive`")
        ).alt(cast_exception),
        lambda _: _factory.failure(
            ValueError("Expected `JsonObj` not `FrozenList[JsonValue]`")
        ).alt(cast_exception),
        lambda d: _factory.success(d),
    )


@dataclass(frozen=True)
class UnfoldedFactory:
    "Factory of unfolded `JsonValue` objects"

    @staticmethod
    def from_list(
        raw: Union[List[Primitive], FrozenList[Primitive]]
    ) -> FrozenList[JsonValue]:
        return _common.from_list(raw)

    @staticmethod
    def from_dict(
        raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
    ) -> JsonObj:
        return _common.from_dict(raw)

    @staticmethod
    def from_unfolded_dict(
        raw: Union[
            Dict[str, RawUnfoldedJsonValue],
            FrozenDict[str, RawUnfoldedJsonValue],
        ]
    ) -> JsonObj:
        return FrozenDict(
            {
                key: JsonValueFactory.from_unfolded(val)
                for key, val in raw.items()
            }
        )

    @staticmethod
    def from_unfolded_list(
        raw: Union[
            List[RawUnfoldedJsonValue], FrozenList[RawUnfoldedJsonValue]
        ]
    ) -> FrozenList[JsonValue]:
        return tuple(JsonValueFactory.from_unfolded(item) for item in raw)

    @staticmethod
    def from_raw_dict(raw: Dict[str, Any]) -> ResultE[JsonObj]:  # type: ignore[misc]
        err = Result.failure(
            cast_exception(TypeError("Not a `JsonObj`")), JsonObj
        )
        return JsonValueFactory.from_any(raw).bind(  # type: ignore[misc]
            lambda jv: jv.map(
                lambda _: err,
                lambda _: err,
                lambda x: Result.success(x),
            )
        )

    @staticmethod
    def loads(raw: str) -> ResultE[JsonObj]:
        return JsonValueFactory.loads(raw).bind(_only_json_objs)

    @staticmethod
    def load(raw: IO[str]) -> ResultE[JsonObj]:
        return JsonValueFactory.load(raw).bind(_only_json_objs)
