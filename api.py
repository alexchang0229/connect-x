"""
This file contains the API for the Connect game. 

TO DO
-----
Implement the following functions:
    - get_name: return your name as a string
    - play: play a move in the game of Connect
"""



import numpy as np


def get_name():
    pass

def play(board: np.ndarray, length_to_win: int) -> int:
    """
    Play a move in the game of Connect.

    How does the board represent the game state?
    -------------------------------------------
    The board is represented in cartesian coordinates with indexes starting at 0.
    Ex: 
    board[0][0] is the bottom left corner of the board.
        [_, _, _, _]
        [_, _, _, _]
        [_, _, _, _]
        [x, _, _, _]

    board[3][0] is the bottom right corner of the board.
        [_, _, _, _]
        [_, _, _, _]
        [_, _, _, _]
        [_, _, _, x]
    
    board[0][3] is the top left corner of the board.
        [x, _, _, _]
        [_, _, _, _]
        [_, _, _, _]
        [_, _, _, _]

    board[3][3] is the top right corner of the board.
        [_, _, _, x]
        [_, _, _, _]
        [_, _, _, _]
        [_, _, _, _]
        

    Args: 
        board: a 2D numpy array representing the game board.

    Returns:
        An integer representing the column in which to play the next move. The column is 0-indexed.
    """
    pass









### Example of how to use ConnectTesta ###
from main.connect import Connect, ConnectTesta
import numpy as np
import random
from competition.week_1 import weak_1_ncc_play_winning_move as ncc_play

def random_agent_1(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def random_agent_2(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

if __name__ == "__main__":
    testa = ConnectTesta("agent_1", random_agent_1, ncc_play.get_name(), ncc_play.play)
    testa.play_automatic_game_with_visual(7, 6, 4, "agent_1", 1)