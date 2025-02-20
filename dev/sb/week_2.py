import numpy as np
import copy
from mcts import mcts

from src.main.connect import ConnectXMatch, GameState


def get_match_object(board: np.ndarray, win_length: int, player: str, opponent: str) -> ConnectXMatch:
    match: ConnectXMatch = ConnectXMatch(board.shape[0], board.shape[1], win_length, player, opponent)
    match.board = board
    # If all elements are None, then no previous player
    if np.all(board == None):
        match.previous_player_who_played = None
    else:
        match.previous_player_who_played = opponent
    return match
    

def get_winning_move(match: ConnectXMatch, player: str) -> int:
    if match.game_state != GameState.IN_PROGRESS:
        return None
    for column in range(match.COLUMNS):
        match_copy: ConnectXMatch = copy.deepcopy(match)
        match_copy.make_move(column, player)
        if match_copy.game_state == GameState.WIN:
            return column
    return None

        

def play_using_mcts(board: np.ndarray, length_to_win: int, opponent_name: str) -> int:
    match: ConnectXMatch = get_match_object(board, length_to_win, "X", opponent_name)
    mcts_instance = mcts(timeLimit=1000)
    bestAction = mcts_instance.search(initialState=match)
    return bestAction