from __future__ import annotations

from typing import Sequence

from typing_extensions import final

from chalk.operators import StaticExpression, StaticOperator
from chalk.operators._column import ColumnExpression
from chalk.operators._literal import LiteralExpression


def _get_name_for_expression(expr: StaticExpression) -> str:
    if isinstance(expr, LiteralExpression):
        if expr.name is None:
            raise ValueError("Literal expressions must have a name")
        return expr.name
    if isinstance(expr, ColumnExpression):
        return expr.final_name()
    raise ValueError("Unknown expression type")


@final
class SelectOperator(StaticOperator):
    def __init__(self, parent: StaticOperator, expressions: Sequence[StaticExpression]):
        self.column_names = tuple(_get_name_for_expression(expr) for expr in expressions)
        self.parent = parent
        self.expressions = expressions

        super().__init__()
