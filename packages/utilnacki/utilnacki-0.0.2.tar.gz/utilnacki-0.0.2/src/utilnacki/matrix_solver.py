from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Any, Sequence

class Direction(Enum):
    ROW = auto()
    COLUMN = auto()
    DIAGONAL = auto()


@dataclass
class MatrixSolver:
    m: list[Sequence[Any]]
    row_cnt: int = field(init=False)
    col_cnt: int = field(init=False)
    size: tuple = field(init=False)
    streak_length: int = 2

    def __post_init__(self):
        self.row_cnt = len(self.m)
        self.col_cnt = max([len(r) for r in self.m])
        self.size = (self.row_cnt, self.col_cnt)
        if self.row_cnt < 3 or self.col_cnt < 3:
            raise ValueError('MatrixSolver must be at least 3x3')
        if self.row_cnt != self.col_cnt:
            raise ValueError('MatrixSolver must have identical height & width')
        if not 2 < self.streak_length <= self.row_cnt:
            raise ValueError('MatrixSolver must have a streak between 2 (the default) and its size')

    @property
    def rows(self) -> list[list[Any]]:
        """[(1, 2, 3), (1, 2, 3), (1, 2, 3)] -> [[1, 2, 3], [1, 2, 3], [1, 2, 3]]"""
        return [[c for c in r] for r in self.m]

    @property
    def columns(self) -> list[list[Any]]:
        """[(1, 2, 3), (1, 2, 3), (1, 2, 3)] -> [[1, 1, 1], [2, 2, 2], [3, 3, 3]]"""
        return [[self.m[j][i] for j in range(len(self.m))] for i in range(len(self.m[0]))]

    def _extract_row_chunks(self) -> list[tuple]:
        """[1, 2, 3, 4], streak_length == 3 -> [(1, 2, 3), (2, 3, 4),]"""
        lists = [[tuple(r[i:i + self.streak_length]) for i in range(len(r) - self.streak_length + 1)] for r in self.m]
        return [tup for lst in lists for tup in lst]

    def _extract_col_chunks(self) -> list[tuple]:
        lists = [[tuple(r[i:i+self.streak_length]) for i in range(len(r) - self.streak_length+1)] for r in self.columns]
        return [tup for lst in lists for tup in lst]

    def _extract_diagonal_chunks(self):
        diagonals = []

        # Extract forward diagonals (bottom-left to top-right)
        for start_col in range(self.col_cnt - self.streak_length + 1):
            for start_row in range(self.row_cnt - self.streak_length + 1):
                diag = [self.m[start_row + i][start_col + i] for i in range(self.streak_length)]
                diagonals.append(tuple(diag))

        # Extract backward diagonals (top-left to bottom-right)
        for start_col in range(self.streak_length - 1, self.col_cnt):
            for start_row in range(self.row_cnt - self.streak_length + 1):
                diag = [self.m[start_row + i][start_col - i] for i in range(self.streak_length)]
                diagonals.append(tuple(diag))

        return diagonals

    def get_streaks(self, directions: Direction | list[Direction] = None) -> list[tuple]:
        """Provide an optional list of Directions.  If no Direction is provided, use Row, Column, and Diagonal.
        [[1, 1, 1], [0, 1, 0], [0, 0, 1]] -> [(1, 1, 1), (1, 1, 1)],
        because there's a streak in the 1st row and one diagonal"""
        if not directions:
            directions = [v for k, v in Direction.__members__.items()]
        directions = [directions] if not isinstance(directions, list) else directions

        d = {Direction.ROW: self._extract_row_chunks(),
             Direction.COLUMN: self._extract_col_chunks(),
             Direction.DIAGONAL: self._extract_diagonal_chunks()}

        return [chunk for direction in directions for chunk in d[direction] if len(set(chunk)) == 1]

    def get_streak_cnt_by_value(self, directions: Direction | list[Direction] = None) -> dict[Any: int]:
        """Same as get_streaks, except [(1, 1, 1), (1, 1, 1)] is returned as {1: 2}"""
        if not directions:
            directions = [v for k, v in Direction.__members__.items()]
        directions = [directions] if not isinstance(directions, list) else directions

        streaks = self.get_streaks(directions)
        streaks_by_value = {s[0]: 0 for s in streaks}
        for s in streaks:
            streaks_by_value[s[0]] += 1

        return streaks_by_value
