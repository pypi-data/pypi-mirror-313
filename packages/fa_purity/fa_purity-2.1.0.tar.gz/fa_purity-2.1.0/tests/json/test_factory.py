from fa_purity import (
    FrozenTools,
)
from fa_purity._core.unsafe import (
    Unsafe,
)
from fa_purity.json import (
    JsonPrimitiveFactory,
    JsonValue,
    JsonValueFactory,
    Primitive,
    Unfolder,
)


def _prim_value(value: Primitive) -> JsonValue:
    return JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(value))


def test_from_any() -> None:
    json_obj = FrozenTools.freeze(
        {
            "foo": JsonValue.from_json(
                FrozenTools.freeze(
                    {
                        "nested": JsonValue.from_list(
                            tuple([_prim_value("hi"), _prim_value(99)])
                        ),
                    }
                )
            )
        }
    )
    json_obj_from_raw = (
        JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}})
        .bind(Unfolder.to_json)
        .alt(Unsafe.raise_exception)
        .to_union()
    )
    assert json_obj == json_obj_from_raw
