#tic_tac_toe/logic/validators.py

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING: #Solves circular imports
    from tic_tac_toe.game.players import Player
    from tic_tac_toe.logic.models import GameState, Grid, Mark

import re

from tic_tac_toe.logic.exceptions import InvalidGameState


#Error handling if something other than an x, 0 or " " slips its way into the grid
def validate_grid(grid: Grid) -> None:
    if not re.match(r"^[\sX0]{9}$", grid.cells):
        raise ValueError("Must contain 9 cells of: X, 0, or spaces")
    


def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(
        game_state.grid, game_state.starting_mark, game_state.winner
    )

def validate_number_of_marks(grid: Grid) -> None: 
    if abs(grid.x_count - grid.o_count) > 1: 
        raise InvalidGameState("Wrong number of X's and 0's")
    
def validate_starting_mark(grid: Grid) -> None:
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and 0s")
    
def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Wrong starting mark")
    elif grid.o_count > grid.x_count:
        if starting_mark != "0":
            raise InvalidGameState("Wrong starting mark")
        
def validate_winner(
    grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
    elif winner == "0":
        if starting_mark == "0":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of 0s")
        else: 
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of 0s")
            
def validate_players(player1: Player, player2: Player) -> None:
    if player1.mark is player2.mark:
        raise ValueError("Players must use different marks")