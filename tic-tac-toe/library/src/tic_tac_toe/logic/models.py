#tic_tac_toe/logic/models.py

from __future__ import annotations
import enum
import re
from dataclasses import dataclass
from functools import cached_property

WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

#Define our two gamepieces
class Mark(enum.StrEnum):
    CROSS = "X"
    NAUGHT = "0"

    @property #define other() function for getting the other Mark
    def other(self) -> Mark:
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT
    

@dataclass(frozen=True)
class Grid:
    cells: str =" " * 9

    #Error handling if something other than an x, 0 or " " slips its way into the grid
    def __post_init__(self) -> None:
        if not re.match(r"^[\sX0]{9}$", self.cells):
            raise ValueError("Must contain 9 cells of: X, 0, or space")
    
    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")
    
    @cached_property
    def o_count(self) -> int:
        return self.cells.count("0")
    
    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")
    
@dataclass(frozen=True)
class Move: 
    mark: Mark                  #moving players mark
    cell_index: int             #index of cell
    before_state: GameState     #state before move
    after_state: GameState      #state after

@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark("X")

    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.x_count == self.grid.o.count:
            return self.starting_mark
        else:
            return self.starting_mark.other
        
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0
    
    @cached_property
    def winner(self) -> Mark | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None    
    
    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?" , mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []
            
