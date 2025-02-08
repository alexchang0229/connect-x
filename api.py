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
from main.connect import ConnectXMatch
import numpy as np
import random
from competition.week_1 import weak_1_ncc_play_winning_move as ncc_play

unit_vectors = [
    [0, 1],
    [1, 0],
    [1, 1],
    [0, -1],
    [-1, 0],
    [-1, 1],
    [1, -1],
    [-1, -1],
]


def heuritic(board, win_length):
    if "heuritic" not in board:
        # random for first move
        return random.randint(0, board.shape[0] - 1)

    board_width = len(board)
    board_height = len(board[0])

    cell_scores = np.zeros((board_width, board_height))
    for y in range(board_width):
        for x in range(board_height):

            how_many_in_a_row = []
            for vector in unit_vectors:
                count = 0
                for head in range(0, 4):
                    head_x = x + head * vector[1]
                    head_y = y + head * vector[0]
                    if head_x >= board_height or head_y >= board_width:
                        break
                    if head_x < 0 or head_y < 0:
                        break
                    pos = board[head_y][head_x]
                    if pos == "heuritic":
                        count += 1
                    elif type(pos) == str:
                        break
                how_many_in_a_row.append(count)
                score = max(how_many_in_a_row)

                if x > 0:
                    if board[y][x - 1] == None:
                        # no floating pieces
                        score = 0
                if board[y][x] != None:
                    # Occupied spot
                    score = 0

                cell_scores[y][x] = score
    max_score_index = np.unravel_index(
        np.argmax(cell_scores, axis=None), cell_scores.shape
    )
    answer = max_score_index[0]
    return answer


def win_blocker(board):
    board_width = len(board)
    board_height = len(board[0])

    for y in range(board_width):
        for x in range(board_height):
            for vector in unit_vectors:
                count = 0
                for head in range(0, 4):
                    head_x = x + head * vector[1]
                    head_y = y + head * vector[0]
                    if not (0 <= head_x < board_height and 0 <= head_y < board_width):
                        break
                    cell = board[head_y][head_x]
                    if cell == None:
                        break
                    if cell != "random_agent_2":
                        count += 1
                    else:
                        break
                if count == 3:
                    head = 3
                    head_x = x + head * vector[1]
                    head_y = y + head * vector[0]
                    if 0 <= head_x < board_height and 0 <= head_y < board_width:
                        if board[head_y][head_x] == None:
                            return (head_y, head_x)
    return


def columnator(board, win_length):
    if "columnator" not in board:
        # random for first move
        return random.randint(0, board.shape[0] - 1)
    print(win_blocker(board))

    column_counts = []
    for col_ind, column in enumerate(board):
        count = 0
        for slot in column:
            if slot == "columnator":
                count += 1
        column_counts.append((col_ind, count))

    column_counts.sort(key=lambda x: x[1], reverse=True)
    sorted_columns = [col[0] for col in column_counts]

    for column_ind in sorted_columns:
        count = 0
        empties = 0
        for slot in board[column_ind]:
            if slot == "columnator":
                count += 1
            elif type(slot) == str:
                count = 0
            else:
                empties += 1
        if empties + count > 4:
            return column_ind


def random_agent_2(board, win_length):
    # Random agent that picks a random column
    if win_blocker(board):
        return win_blocker(board)[0]
    return random.randint(0, board.shape[0] - 1)
