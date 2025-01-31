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
