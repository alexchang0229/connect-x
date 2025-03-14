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


def play(board: np.ndarray, length_to_win: int, opponent_name: str) -> int:
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






####################################################################################################
# EXAMPLES #
####################################################################################################
from src.main.connect import Matchup, ConnectXVisual, Agent, BoardDimension, MetaMatchup, Tournament
import numpy as np
import random



##### Example: Defining an agent #####
# Simple agent that always picks the first available column
def get_first_column_name():
    return "First Column Agent"
def agent_first_column(board, win_length, opponent_name):
    return 0

# Random agent that picks a random column
def get_random_agent_1_name():
    return "Random Agent 1"
def random_agent_1(board, win_length, opponent_name):
    return random.randint(0, board.shape[0] - 1)

# Simple agent that always picks the last available column
def get_last_column_name():
    return "Last Column Agent"
def agent_last_column(board, win_length, opponent_name):
    return board.shape[0] - 1


##### Example: Playing a matchup between multiple agents #####
# Create a matchup
number_of_games = 10
board_dim = BoardDimension(7, 6)
agent_1 = Agent(get_first_column_name(), agent_first_column)
agent_2 = Agent(get_random_agent_1_name(), random_agent_1)
matchup: Matchup = Matchup(
    board_dim,
    4,
    agent_1,
    agent_2,
    1,
    5
)
# Play a matchup
matchup.play_n_games(number_of_games)
# Generate a report
matchup.generate_report("first_column_vs_random_agent_1.txt")


##### Example: Playing a metamatchup between multiple agents #####
# The metamatchup allows to easily play multiple matchups with different board dimensions and win lengths.
board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
win_lengths = [4, 5]
first_agent = Agent("First Column", agent_first_column)
second_agent = Agent("Random Agent 1", random_agent_1)
meta_matchup: MetaMatchup = MetaMatchup(
    board_dimensions,
    win_lengths,
    first_agent,
    second_agent,
    turn_time_limit_s=1,
    win_percentage_threshold_for_win=5,
    number_of_games_per_matchup=10
)
# Play the metamatchup
meta_matchup.play_matchups()
# Generate a report
meta_matchup.generate_report("meta_first_column_vs_random_agent_1.txt")


##### Example: Playing a tournament #####
# The tournament allows to easily play multiple metamatchups with different agents.
# Create a tournament
board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
win_lengths = [4, 5]
agents = [
    Agent("First Column", agent_first_column),
    Agent("Random Agent 1", random_agent_1),
    Agent("Last Column", agent_last_column)
]
tournament: Tournament = Tournament(
    board_dimensions,
    win_lengths,
    agents,
    turn_time_limit_s=1,
    win_percentage_threshold_for_win=5,
    number_of_games_per_matchup=10
)
# Play the tournament
tournament.play_tournament()
# Generate a report
tournament.generate_reports_in_dir("test_tournament_reports")

##### Visualizing the game ######
# # Playing a game manually 
# visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_manual_game("X", "O")

# # Play a game against an agent
# visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_manual_against_agent("Human", "AI", agent_first_column, True, 1, 0.2)

# # Visualize a game between two agents
# visual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_real_time_game("X", "O", agent_first_column, random_agent_1, 1, 2)

# # Visualize X games between two agents (will alternate the starting player)
# visual = ConnectXVisual(7, 6, 4, 100, 100)
# agent_1: Agent = Agent("Agent1", agent_first_column)
# agent_2: Agent = Agent("Agent2", random_agent_1)
# visual.play_multiple_real_time_games(agent_1, agent_2, 1, 2, 3)