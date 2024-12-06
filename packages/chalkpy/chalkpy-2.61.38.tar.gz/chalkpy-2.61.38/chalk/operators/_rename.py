from __future__ import annotations

import collections.abc
from typing import Mapping, Sequence

from typing_extensions import final

from chalk.operators import StaticOperator


@final
class RenameOperator(StaticOperator):
    def __init__(self, parent: StaticOperator, names: Sequence[str] | Mapping[str, str]):
        """Rename the columns of the table, given a Mapping of {from: to}, or an list with the same number of columns"""
        super().__init__()
        if not isinstance(names, collections.abc.Mapping):
            names = tuple(names)
            if len(names) != len(parent.column_names):
                raise ValueError("If a list is given, the names must be the same length")
            names = {k: v for (k, v) in zip(parent.column_names, names)}
        if not isinstance(names, collections.abc.Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("The names must be a mapping of {from: to} or a list")
        for column in names:
            if column not in parent.column_names:
                raise ValueError(f"Column '{column}' is not in the table")
        new_column_names: dict[str, None] = {}  # Using this like an ordered set
        for column in parent.column_names:
            if column in names:
                new_name = names[column]
                if new_name in new_column_names:
                    raise ValueError(f"Column '{new_name}' would appear multiple times in the new table")
                # We are not dropping this column
                new_column_names[new_name] = None
            else:
                if column in new_column_names:
                    raise ValueError(f"Column '{column}' would appear multiple times in the new table")
                new_column_names[column] = None
        self.column_names = tuple(new_column_names)
        self.parent = parent
        self.old_name_to_new_name_map = names
