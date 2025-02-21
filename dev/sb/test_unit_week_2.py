import numpy as np
import pytest
import random

from dev.sb.week_2 import get_winning_move, get_match_object, play_using_mcts
from src.main.connect import (
    GameState, 
    ConnectXMatch, 
    ConnectXMatchWithAgents, 
    Matchup, 
    MetaMatchup, 
    ConnectXVisual, 
    BoardDimension, 
    Agent,
    Tournament
)
from competition.week_2.agents.threshold_week_2 import heuritic, columnator


@pytest.fixture
def match():
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    return match


def test_get_match_object_empty_board():
    board = np.full((7, 6), None)
    win_length = 4
    player = "X"
    opponent = "O"
    match = get_match_object(board, win_length, player, opponent)
    
    assert isinstance(match, ConnectXMatch)
    assert match.COLUMNS == 7
    assert match.ROWS == 6
    assert match.WIN_LENGTH == 4
    assert match.FIRST_PLAYER_NAME == player
    assert match.SECOND_PLAYER_NAME == opponent
    assert match.previous_player_who_played is None

def test_get_match_object_non_empty_board():
    match = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "X")
    match.make_move(1, "O")
    board = match.board
    win_length = 4
    player = "X"
    opponent = "O"
    match_from_function = get_match_object(board, win_length, player, opponent)
    
    assert isinstance(match_from_function, ConnectXMatch)
    assert match_from_function == match
    

def test_get_winning_move():
    # Simulate a situation where player "X" can win
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "X")
    match.make_move(1, "X")
    match.make_move(2, "X")
    winning_move = get_winning_move(match, "X")
    assert winning_move == 3

    # Simulate a situation where player "O" can win
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "O")
    match.make_move(1, "O")
    match.make_move(2, "O")
    winning_move = get_winning_move(match, "O")
    assert winning_move == 3

    # Simulate a situation where no winning move is available
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "X")
    match.make_move(1, "O")
    match.make_move(2, "X")
    match.make_move(3, "O")
    winning_move = get_winning_move(match, "X")
    assert winning_move is None

    # Simulate vertical winning move
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "X")
    match.make_move(0, "X")
    match.make_move(0, "X")
    winning_move = get_winning_move(match, "X")
    assert winning_move == 0

    # Simulate diagonal winning move
    match: ConnectXMatch = ConnectXMatch(7, 6, 4, "X", "O")
    match.make_move(0, "X")
    match.make_move(1, "O")
    match.make_move(1, "X")
    match.make_move(2, "O")
    match.make_move(2, "O")
    match.make_move(2, "X")
    match.make_move(3, "O")
    match.make_move(3, "O")
    match.make_move(3, "O")
    winning_move = get_winning_move(match, "X")
    assert winning_move == 3

    # Simulate board is full
    match: ConnectXMatch = ConnectXMatch(1, 1, 4, "X", "O")
    match.make_move(0, "X")
    winning_move = get_winning_move(match, "X")
    assert winning_move is None


def random_agent_1(board, win_length, opponent_name):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def test_unit_mcts():
    # board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
    board_dimensions = [BoardDimension(7, 6)]
    # win_lengths = [4, 5]
    win_lengths = [4]
    first_agent = Agent("Faithful", play_using_mcts)
    second_agent = Agent("Agent2", random_agent_1)
    meta_matchup: MetaMatchup = MetaMatchup(
        board_dimensions,
        win_lengths,
        first_agent,
        second_agent,
        turn_time_limit_s=5,
        win_percentage_threshold_for_win=10,
        number_of_games_per_matchup=10
    )
    meta_matchup.play_matchups()
    print("hello")

def test_unit_mcts_stronger_players():
    # board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
    board_dimensions = [BoardDimension(7, 6), BoardDimension(7, 6), BoardDimension(7, 6), BoardDimension(7, 6)]
    # win_lengths = [4, 5]
    win_lengths = [4]
    first_agent = Agent("Faithful", play_using_mcts)
    second_agent = Agent("Heuritic", heuritic)
    meta_matchup: MetaMatchup = MetaMatchup(
        board_dimensions,
        win_lengths,
        first_agent,
        second_agent,
        turn_time_limit_s=5,
        win_percentage_threshold_for_win=10,
        number_of_games_per_matchup=1
    )
    meta_matchup.play_parallel_matchups()
    meta_matchup.generate_report("test.txt")
    print("hello")