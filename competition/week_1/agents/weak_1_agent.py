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
    return "weak_1"

def play(board: np.ndarray, length_to_win: int) -> int:
    # Get the number of columns and rows
    columns = board.shape[0]
    rows = board.shape[1]

    # Randomly choose a column
    column = np.random.randint(columns)

    return column