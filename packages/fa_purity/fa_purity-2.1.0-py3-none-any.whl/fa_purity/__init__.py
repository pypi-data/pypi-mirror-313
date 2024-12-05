"Pure functional and typing utilities"
from ._core.bool import (
    Bool,
)
from ._core.cmd import (
    Cmd,
    CmdUnwrapper,
)
from ._core.coproduct import (
    Coproduct,
    CoproductFactory,
    UnionFactory,
)
from ._core.frozen import (
    FrozenDict,
    FrozenList,
    FrozenTools,
)
from ._core.maybe import (
    Maybe,
)
from ._core.pure_iter import (
    PureIter,
    PureIterFactory,
)
from ._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from ._core.stream import (
    Stream,
    StreamFactory,
)
from ._core.unit import (
    unit,
    UnitType,
)
from ._core.unsafe import (
    Unsafe,
)
from ._core.utils import (
    cast_exception,
)
from ._transform.cmd import (
    CmdTransform,
)
from ._transform.coproduct import (
    CoproductTransform,
)
from ._transform.pure_iter import (
    PureIterTransform,
)
from ._transform.result import (
    ResultTransform,
)
from ._transform.stream import (
    StreamTransform,
)

__version__ = "2.1.0"
__all__ = [
    "Bool",
    # ---
    "Cmd",
    "CmdTransform",
    "CmdUnwrapper",
    # ---
    "Coproduct",
    "CoproductFactory",
    "CoproductTransform",
    "UnionFactory",
    # ---
    "FrozenDict",
    "FrozenList",
    "FrozenTools",
    # ---
    "Maybe",
    # ---
    "PureIter",
    "PureIterFactory",
    "PureIterTransform",
    # ---
    "Result",
    "ResultE",
    "ResultFactory",
    "ResultTransform",
    # ---
    "Stream",
    "StreamFactory",
    "StreamTransform",
    # ---
    "unit",
    "UnitType",
    # ---
    "Unsafe",
    # ---
    "cast_exception",
]
