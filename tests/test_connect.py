import unittest
import pytest
import tkinter as tk
import random

from main.connect import GameState, ConnectXMatch, ConnectXMatchWithAgents, ConnectXMatchup, ConnectXVisual

@pytest.fixture
def game():
    return ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")

class TestConnectXMatch:
    def test_check_illegal_move(self, game: ConnectXMatch):
        # Ensure an illegal move is detected
        game.make_move(0, 'X')

        # Wrong name
        with pytest.raises(Exception):
            game.make_move(0, 'Y')

        # Play in terminal state
        game.game_state = GameState.DRAW
        with pytest.raises(Exception):
            game.make_move(0, 'X')

        # Play outside of the board
        game: ConnectXMatch = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.play_with_next_player(-1)
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played is 'X'
        
        # Play in a full column
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for _ in range(6):
            game.play_with_next_player(0)
        game.play_with_next_player(1)
        game.play_with_next_player(0)
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "X"
        assert game.previous_player_who_played is 'O'

        # Play None
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(None, "X")
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played is 'X'

        # Play String
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move("string", "X")
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played is 'X'


    def test_horizontal_win(self, game: ConnectXMatch):
        # Simulate a horizontal win
        for col in range(4):
            assert not game.check_win()
            game.make_move(col, 'X')
        assert game.check_win()

    def test_vertical_win(self, game: ConnectXMatch):
        # Simulate a vertical win
        for row in range(4):
            assert not game.check_win()
            game.make_move(0, 'X')
        assert game.check_win()

    def test_diagonal_win(self, game: ConnectXMatch):
        # Simulate a diagonal win
        for i in range(4):
            assert not game.check_win()
            for j in range(i):
                game.make_move(i, 'O')
            game.make_move(i, 'X')
        assert game.check_win()

    def test_anti_diagonal_win(self, game: ConnectXMatch):
        # Simulate an anti-diagonal win
        for i in range(4):
            for j in range(3 - i):
                game.make_move(i, 'O')
            game.make_move(i, 'X')
        assert game.check_win()

    def test_no_win(self, game: ConnectXMatch):
        # Ensure no win is detected when there is no win
        game.make_move(0, 'X')
        game.make_move(1, 'X')
        game.make_move(2, 'X')
        assert not game.check_win()

    def test_corner_win(self, game: ConnectXMatch):
        ## Bottom left corner
        # Simulate columns win in the bottom-left corner
        for row in range(4):
            game.make_move(0, 'X')
            if row < 3:
                assert not game.check_win()
        assert game.check_win()
        # Simulate row win in the bottom-left corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for col in range(4):
            game.make_move(col, 'X')
            if col < 3:
                assert not game.check_win()
        assert game.check_win()

        ## Bottom right corner
        # Simulate columns win in the bottom-right corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for row in range(4):
            game.make_move(game.COLUMNS - 1, 'X')
            if row < 3:
                assert not game.check_win()
        assert game.check_win()
        # Simulate row win in the bottom-right corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for col in range(4):
            game.make_move(game.COLUMNS - 1 - col, 'X')
            if col < 3:
                assert not game.check_win()
        assert game.check_win()

        ## Top left corner
        # Simulate columns win in the top-left corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for row in range(4):
            game.board[0][-1-row] = 'X'
            if row < 3:
                assert not game.check_win()
        assert game.check_win()
        # Simulate row win in the top-left corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for col in range(4):
            game.board[col][-1] = 'X'
            if col < 3:
                assert not game.check_win()
        assert game.check_win()

        ## Top right corner
        # Simulate columns win in the top-right corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for row in range(4):
            game.board[-1][-1-row] = 'X'
            if row < 3:
                assert not game.check_win()
        assert game.check_win()
        # Simulate row win in the top-right corner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for col in range(4):
            game.board[-1-col][-1] = 'X'
            if col < 3:
                assert not game.check_win()
        assert game.check_win()

    def test_draw(self, game: ConnectXMatch):
        game.WIN_LENGTH = 10
        # Simulate a draw
        for col in range(7):
            for row in range(6):
                assert not game.check_draw()
                game.make_move(col, 'X')
        assert game.check_draw()

    def test_make_move(self, game: ConnectXMatch):
        # Test making a valid move
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(0, 'X')
        assert game.board[0][0] == 'X'
        assert game.game_state == GameState.IN_PROGRESS
        assert game.winner is None
        assert game.previous_player_who_played is 'X'

        # Test making a move with wrong name
        with pytest.raises(Exception):
            game.make_move(0, 'Y')

        # Test making a move in a terminal state (win)
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.game_state = GameState.WIN
        with pytest.raises(Exception):
            game.make_move(0, 'X')
        
        # Test making a move in a full column
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.WIN_LENGTH = 10
        for _ in range(6):
            game.make_move(0, 'O')
        game.make_move(0, 'X')
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played is 'X'
        
        # Test making a move outside the board
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(-1, 'X')
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played is 'X'

        # Test getting a winner
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(0, 'X')
        game.make_move(1, 'X')
        game.make_move(2, 'X')
        game.make_move(3, 'X')
        assert game.game_state == GameState.WIN
        assert game.winner == 'X'
        assert game.previous_player_who_played == 'X'
        
        # Test making a draw
        game = ConnectXMatch(columns=2, rows=2, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(0, 'X')
        game.make_move(1, 'O')
        game.make_move(0, 'X')
        game.make_move(1, 'O')
        assert game.check_draw()
        assert game.game_state == GameState.DRAW
        assert game.winner is None
        assert game.previous_player_who_played == 'O'

    def test_play_with_next_player(self, game: ConnectXMatch):
        # Test playing with the next player
        game.play_with_next_player(0)
        assert game.board[0][0] == 'X'
        assert game.game_state == GameState.IN_PROGRESS
        assert game.winner is None
        assert game.previous_player_who_played == 'X'

        game.play_with_next_player(1)
        assert game.board[1][0] == 'O'
        assert game.game_state == GameState.IN_PROGRESS
        assert game.winner is None
        assert game.previous_player_who_played == 'O'

        # Test playing with the next player in a full column
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.WIN_LENGTH = 10
        for _ in range(6):
            game.play_with_next_player(0)
        game.play_with_next_player(0)
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner is "O"
        assert game.previous_player_who_played == 'X'

        # Test playing with the next player in a terminal state (win)
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.game_state = GameState.WIN
        with pytest.raises(Exception):
            game.play_with_next_player(0)

        # Test playing with the next player in a terminal state (draw)
        game = ConnectXMatch(columns=2, rows=2, win_length=4, first_player_name="X", second_player_name="O")
        game.play_with_next_player(0)
        game.play_with_next_player(1)
        game.play_with_next_player(0)
        game.play_with_next_player(1)
        assert game.check_draw()
        assert game.game_state == GameState.DRAW
        assert game.winner is None
        assert game.previous_player_who_played == 'O'



def agent_first_column(board, win_length):
    # Simple agent that always picks the first available column
    return 0
def agent_last_column(board, win_length):
    # Simple agent that always picks the last available column
    return board.shape[0] - 1
        
def agent_empty(board, win_length):
    # Finds the first empty column and plays there
    # Otherwise random
    for col in range(board.shape[0]):
        if board[col][0] is None:
            return col
    return random.randint(0, board.shape[0] - 1)

def random_agent_1(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def random_agent_2(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)


class TestConnectXMatchWithAgents:
    def test_play_move_with_agent(self):
        match: ConnectXMatchWithAgents = ConnectXMatchWithAgents(
            7,
            6,
            4,
            "X", 
            "O",
            agent_first_column, 
            agent_last_column,
            5
        )
        assert match.play_move_with_agent("X")
        assert match.game.game_state == GameState.IN_PROGRESS
        assert match.game.board[0][0] == "X"
        assert match.play_move_with_agent("O")
        assert match.game.game_state == GameState.IN_PROGRESS
        assert match.game.board[6][0] == "O"
        assert match.play_move_with_agent("X")
        assert match.play_move_with_agent("X")
        assert not match.play_move_with_agent("X")
        assert match.game.game_state == GameState.WIN
        assert match.game.winner == "X"
        assert match.game.previous_player_who_played == "X"

    def test_play_move_with_next_agent(self):
        match: ConnectXMatchWithAgents = ConnectXMatchWithAgents(
            7,
            6,
            4,
            "X", 
            "O",
            agent_first_column, 
            agent_last_column,
            5
        )
        assert match.play_move_with_next_agent()
        assert match.game.game_state == GameState.IN_PROGRESS
        assert match.game.board[0][0] == "X"
        assert match.play_move_with_next_agent()
        assert match.game.game_state == GameState.IN_PROGRESS
        assert match.game.board[6][0] == "O"
        assert match.play_move_with_next_agent()
        assert match.play_move_with_next_agent()
        assert match.play_move_with_next_agent()
        assert match.play_move_with_next_agent()
        assert not match.play_move_with_next_agent()
        assert match.game.game_state == GameState.WIN
        assert match.game.winner == "X"
        assert match.game.previous_player_who_played == "X"

    def test_play_full_game(game):
        match = ConnectXMatchWithAgents(
            7,
            6,
            4,
            "agent_1", 
            "agent_2",
            agent_first_column, 
            agent_last_column,
            5
        )
        assert match.play_full_game() == "agent_1"

        match = ConnectXMatchWithAgents(
            7,
            6,
            4,
            "agent_2", 
            "agent_1",
            agent_first_column, 
            agent_last_column,
            5
        )
        assert match.play_full_game() == "agent_2"






class TestConnectXMatchup:
    def test_play_matchup(self):
        ### Player 1 wins
        matchup: ConnectXMatchup = ConnectXMatchup(
            7,
            6,
            4,
            "agent_1", 
            "agent_2",
            agent_first_column, 
            agent_empty,
            5,
            10,
            10
        )
        # Before
        assert matchup.first_player_wins == 0
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins is None
        assert matchup.percentage_second_player_wins is None
        assert matchup.percentage_draws is None
        assert matchup.winner is None
        # Play the matchup
        matchup.play_matchup()
        # After
        assert matchup.first_player_wins == 10
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 100.0
        assert matchup.percentage_second_player_wins == 0.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner is "agent_1"

        ### Equal strats
        matchup: ConnectXMatchup = ConnectXMatchup(
            7,
            6,
            4,
            "agent_1", 
            "agent_2",
            agent_first_column, 
            agent_last_column,
            5,
            10,
            10
        )
        # Before
        assert matchup.first_player_wins == 0
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins is None
        assert matchup.percentage_second_player_wins is None
        assert matchup.percentage_draws is None
        assert matchup.winner is None
        # Play the matchup
        matchup.play_matchup()
        # After
        assert matchup.first_player_wins == 5
        assert matchup.second_player_wins == 5
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 50.0
        assert matchup.percentage_second_player_wins == 50.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'

    def test_generate_report(self):
        matchup: ConnectXMatchup = ConnectXMatchup(
            7,
            6,
            4,
            "agent_1", 
            "agent_2",
            agent_first_column, 
            agent_last_column,
            5,
            10,
            10
        )
        # Play the matchup
        matchup.play_matchup()
        # Generate the report
        matchup.generate_report("test_report.txt")      


class TestConnectXVisual:
    def test_manual_start(self):
        visual = ConnectXVisual(7, 6, 4)
        visual.play_manual_game("X", "O")

    def test_play_real_time_game(self):
        visual = ConnectXVisual(7, 6, 4)
        visual.play_real_time_game("X", "O", agent_first_column, agent_last_column, 1)



if __name__ == "__main__":
    unittest.main()
