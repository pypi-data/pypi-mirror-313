from typing import Any

import pyarrow as pa

from chalk.operators import StaticExpression


class LiteralExpression(StaticExpression):
    def __init__(self, value: Any, dtype: pa.DataType, name: str | None = None) -> None:
        super().__init__()
        self.value = value
        self.dtype = dtype
        self.name = name

        super().__init__()

    def alias(self, name: str) -> StaticExpression:
        return LiteralExpression(self.value, self.dtype, name)
