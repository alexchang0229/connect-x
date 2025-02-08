"""
This file contains the API for the Connect game. 

TO DO
-----
Implement the following functions:
    - get_name: return your name as a string
    - play: play a move in the game of Connect
"""



import numpy as np


def test_move(board_copy,column,name):
    column_to_play = board_copy[column]
    
    # Find the first occurrence of None
    none_index = np.where(column_to_play == None)[0]  # Get indices where values are None

    if none_index.size > 0:  # Check if at least one None exists
        column_to_play[none_index[0]] = name  # Replace the first None
    
    board_copy[column] = column_to_play
    return board_copy

def check_for_win(new_board,length_to_win,name):
    columns = new_board.shape[0]
    rows = new_board.shape[1]
    
    #Check horizontal
    for row in range(columns-length_to_win):
        for col in range(rows):
            line = list(new_board[row:row+length_to_win,col])
            if line.count(name) == length_to_win:
                return True

    #Check vertical
    for columns in range(columns):
        for items in range(rows-length_to_win+1):
            line=list(new_board[columns][items:items+length_to_win])
            if line.count(name) == length_to_win:
                return True


def get_name():
    return "NCC"

def play(board: np.ndarray, length_to_win: int) -> int:
    # Get the number of columns and rows
    columns = board.shape[0]
    rows = board.shape[1]
    
    name = "NCC"
    opponent = "agent_1"
    board_copy = board.copy()
    for column in range(columns):
        new_board = test_move(board_copy,column, name)
        #Check for win
        if(check_for_win(new_board,length_to_win,name)):
            return column
        
        if(check_for_win(new_board, length_to_win,opponent)):
            backup_move = True
            blocking_move = column
        
    if backup_move:
        return blocking_move
    else:    
    # Randomly choose a column
        column = np.random.randint(columns)
        return column