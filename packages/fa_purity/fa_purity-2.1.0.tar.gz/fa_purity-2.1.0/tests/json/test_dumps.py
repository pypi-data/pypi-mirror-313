from decimal import (
    Decimal,
)
from fa_purity import (
    FrozenTools,
)
from fa_purity.json import (
    JsonPrimitiveFactory,
    JsonUnfolder,
    JsonValue,
)


def test_dumps() -> None:
    obj = FrozenTools.freeze(
        {
            "foo": JsonValue.from_primitive(
                JsonPrimitiveFactory.from_raw(Decimal("123.44"))
            )
        }
    )
    expected = '{"foo": 123.44}'
    assert JsonUnfolder.dumps(obj) == expected
