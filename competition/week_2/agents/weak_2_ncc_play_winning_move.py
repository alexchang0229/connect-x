"""
This file contains the API for the Connect game. 

TO DO
-----
Implement the following functions:
    - get_name: return your name as a string
    - play: play a move in the game of Connect
"""




import numpy as np
import copy
import random
import logging
import math

logger = logging.getLogger(__name__)
logging.basicConfig(filename='ncc_agent.log', level=logging.CRITICAL, filemode="w")

def fuzzy_closest(lst, target, randomness=0.75):
    """
    Selects a number from lst that is generally close to target but with some randomness.
    
    randomness: 0 (always closest) to 1 (completely random).
    """
    # Compute distances from the target
    distances = np.abs(np.array(lst) - target)
    
    # Convert distances to weights (closer = higher weight)
    weights = np.exp(-distances / (randomness * distances.std() + 1e-9))  # Avoid div by zero
    
    # Normalize weights to sum to 1
    weights /= weights.sum()
    
    # Randomly pick an element with these weights
    try:
        return random.choices(lst, weights=weights, k=1)[0]
    except:
        return random.choice(lst)

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
    for row in range(columns-length_to_win+1):
        for col in range(rows):
            line = list(new_board[row:row+length_to_win,col])
            if line.count(name) == length_to_win:
                logger.warning("Found Horizontal Win Condition")
                return True

    #Check vertical
    for columns in range(columns):
        for items in range(rows-length_to_win+1):
            line=list(new_board[columns][items:items+length_to_win])
            if line.count(name) == length_to_win:
                logger.warning("Found Vertical Win Condition")

                return True

    # Check positive diagonal (top-left to bottom-right)
    for row in range(rows - length_to_win + 1):
        for col in range(columns - length_to_win + 1):
            line = [new_board[row + i][col + i] for i in range(length_to_win)]
            if line.count(name) == length_to_win:
                logger.warning("Found Positive Diagonal Win Condition")
                return True

    # Check negative diagonal (bottom-left to top-right)
    for row in range(length_to_win - 1, columns):
        for col in range(columns - length_to_win + 1):
            line = [new_board[row - i][col + i] for i in range(length_to_win)]
            if line.count(name) == length_to_win:
                logger.warning("Found Negative Diagonal Win Condition")
                return True
    
    return False
def get_name():
    return "NCC"

def play(board: np.ndarray, length_to_win: int, opponent_name: str) -> int:
    # Get the number of columns and rows
    columns = board.shape[0]
    rows = board.shape[1]
    backup_move = False
    possible_moves = []
    logger.error("NEXT TURN")
    name = get_name()
    for column in range(columns):
        temp_board_name = copy.deepcopy(board)
        new_board = test_move(temp_board_name,column, name)
        #Check for win
        logger.info(f"Checking for own winning move in {column}")
        if(check_for_win(new_board,length_to_win,name)):
            final_move = column
            logger.error(f"Playing winning move in {final_move}")
            return column
        temp_board_opponent = copy.deepcopy(board)
        new_board_opponent = test_move(temp_board_opponent,column, opponent_name)
        logger.info(f"Checking for opponents winning move in {column}")
        if(check_for_win(new_board_opponent, length_to_win,opponent_name)):
            backup_move = True
            blocking_move = column
        if board[column][-1] is None:
                possible_moves.append(column)
        
    if backup_move:
        logger.error(f"playing blocking move in column {blocking_move}")
        return blocking_move
    else:    
    # Randomly choose a VALID column that doesn't lead to win for opponent
        if len(possible_moves) > 0:
            last_resort = possible_moves.copy()
            for move in possible_moves:
                future_board_opponent = copy.deepcopy(board)
                new_board_future = test_move(future_board_opponent, move, name)
                for opponent_moves in range(columns):
                    updated_board_check = copy.deepcopy(new_board_future)
                    updated_board_check = test_move(updated_board_check, opponent_moves, opponent_name)
                    logger.info(f"Checking if move in column {move} leads to win for opponent in column {opponent_moves}")
                    opponent_can_win = check_for_win(updated_board_check, length_to_win,opponent_name)
                    if opponent_can_win is True:
                        possible_moves.remove(move)
                        logger.warning(f"Removing column {move} from list {possible_moves}")
                        break
                    
            if len(possible_moves)>0:
                logger.warning(f"possible moves that won't lead to opponent win are {possible_moves}")
                #Check for move that would lead to three pieces in a row
                for column in possible_moves:
                    three_piece_board_check = copy.deepcopy(board)
                    new_board = test_move(three_piece_board_check,column, name)
                    #Check for win
                    logger.info(f"Checking for own win-1 move in {column}")
                    if(check_for_win(new_board,length_to_win-1,name)):
                        potential_move = column
                        
                        for next_column in possible_moves:
                            future_board = copy.deepcopy(new_board)
                            future_new_board = test_move(future_board,next_column, name)
                            logger.info(f"checking if 3 piece move in {potential_move} can result in win with {next_column}")
                            if(check_for_win(future_new_board,length_to_win,name)):
                                logger.error(f"can win next turn, playing winning-1 move in {potential_move}")
                                return potential_move
                final_move = fuzzy_closest(possible_moves, math.floor(columns/2))
                logger.error(f"playing random move in {final_move}")
                return final_move
            else:
                logger.warning(f"no safe move to play have to play one of {last_resort}")
                move = random.choice(last_resort)
                logger.error(f"playing move in column {move}")
                return move
        else:
            logger.error("No moves to play")
