#tic_tac_toe/logic/models.py

from __future__ import annotations
import enum
import re
from dataclasses import dataclass
from functools import cached_property

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
