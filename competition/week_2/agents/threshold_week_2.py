import numpy as np
import random
import copy

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


def heuritic(board, win_length, opponent_name):
    board = copy.deepcopy(board)

    if "heuritic" not in board:
        # random for first move
        return random.randint(0, board.shape[0] - 1)

    if win_blocker(board, "heuritic"):
        return win_blocker(board, "heuritic")[0]

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
                        count += 1 / (head + 1)
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
    print(answer)
    answer = int(answer)
    return answer


def win_blocker(board, name):
    board_width = len(board)
    board_height = len(board[0])

    for y in range(board_width):
        for x in range(board_height):
            for vector in unit_vectors:
                mine_count = 0
                theirs_count = 0
                for head in range(0, 4):
                    head_x = x + head * vector[1]
                    head_y = y + head * vector[0]
                    if not (0 <= head_x < board_height and 0 <= head_y < board_width):
                        break
                    cell = board[head_y][head_x]
                    if cell != name and cell != None:
                        theirs_count += 1
                    if cell == name:
                        mine_count += 1
                if mine_count == 3 or theirs_count == 3:
                    for head in range(0, 4):
                        head_x = x + head * vector[1]
                        head_y = y + head * vector[0]
                        if 0 <= head_x < board_height and 0 <= head_y < board_width:
                            # if next cell in 3 in a row sequence is in the board
                            if board[head_y][head_x - 1] is not None or head_x == 0:
                                # if the next cell is on the first row or there is a token under it
                                if board[head_y][head_x] == None:
                                    # if it is not currently occupied
                                    return (head_y, head_x)
    return


def columnator(board, win_length, opponent_name):
    board = copy.deepcopy(board)
    if "columnator" not in board:
        # random for first move
        return random.randint(0, board.shape[0] - 1)
    if win_blocker(board, "columnator"):
        return win_blocker(board, "columnator")[0]

    column_counts = []
    for col_ind, column in enumerate(board):
        # Sort columns by how many of my tokens are in each one
        count = 0
        for slot in column:
            if slot == "columnator":
                count += 1
        column_counts.append((col_ind, count))

    column_counts.sort(key=lambda x: x[1], reverse=True)
    sorted_columns = [col[0] for col in column_counts]

    for column_ind in sorted_columns:
        # Go through sorted columns and play token if it can fit 4 in a row
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
