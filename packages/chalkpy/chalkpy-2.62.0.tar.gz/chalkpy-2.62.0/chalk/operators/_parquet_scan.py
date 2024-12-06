from __future__ import annotations

from typing import Sequence

from typing_extensions import final

from chalk.operators import StaticOperator
from chalk.utils.collections import ensure_tuple


@final
class ParquetScanOperator(StaticOperator):
    def __init__(self, files: str | Sequence[str], columns: Sequence[str]):
        super().__init__()
        self.files = ensure_tuple(files)
        self.column_names = ensure_tuple(columns)
