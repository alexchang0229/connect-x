"""
This file contains the API for the Connect game. 

TO DO
-----
Implement the following functions:
    - get_name: return your name as a string
    - play: play a move in the game of Connect
"""



import numpy as np
'''
def check_rows_for_winner(length_to_win,board):
    for rows in board:
        

def check_columns_for_winner(length_to_win,board):

def check_down_right_for_winner(length_to_win,board):

def check_down_left_for_winner(length_to_win,board):
'''
def get_name():
    return "NCC"

def play(board: np.ndarray, length_to_win: int) -> int:
    # Get the number of columns and rows
    columns = board.shape[0]
    rows = board.shape[1]
    # Randomly choose a column
    column = np.random.randint(columns)

    return column