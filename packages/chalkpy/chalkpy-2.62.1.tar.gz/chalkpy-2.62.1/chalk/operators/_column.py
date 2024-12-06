from chalk.operators import StaticExpression


class ColumnExpression(StaticExpression):
    def __init__(self, source_column: str, alias: str | None = None) -> None:
        super().__init__()
        self.source_column = source_column
        self.aliased_name = alias
        super().__init__()

    def alias(self, name: str) -> StaticExpression:
        return ColumnExpression(self.source_column, alias=name)

    def final_name(self) -> str:
        return self.aliased_name or self.source_column
