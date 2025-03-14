import unittest
import pytest
import random
import os
import copy
import numpy as np

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
        assert game.winner == "O"
        assert game.previous_player_who_played == 'X'
        
        # Play in a full column
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        for _ in range(6):
            game.play_with_next_player(0)
        game.play_with_next_player(1)
        game.play_with_next_player(0)
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner == "X"
        assert game.previous_player_who_played == 'O'

        # Play None
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(None, "X")
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner == "O"
        assert game.previous_player_who_played == 'X'

        # Play String
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move("string", "X")
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner == "O"
        assert game.previous_player_who_played == 'X'


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
        assert game.previous_player_who_played == 'X'

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
        assert game.winner == "O"
        assert game.previous_player_who_played == 'X'
        
        # Test making a move outside the board
        game = ConnectXMatch(columns=7, rows=6, win_length=4, first_player_name="X", second_player_name="O")
        game.make_move(-1, 'X')
        assert game.game_state == GameState.ILLEGAL_MOVE
        assert game.winner == "O"
        assert game.previous_player_who_played == 'X'

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
        assert game.winner == "O"
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

    def test_deepcopy(self):
        # Create an instance of ConnectXMatch
        original_match = ConnectXMatch(7, 6, 4, "Player1", "Player2")
        
        # Make some moves
        original_match.make_move(0, "Player1")
        original_match.make_move(1, "Player2")
        original_match.make_move(0, "Player1")
        
        # Create a deep copy of the original match
        copied_match = copy.deepcopy(original_match)
        
        # Check that the copied match is equal to the original match
        assert np.array_equal(original_match.board, copied_match.board)
        assert original_match.game_state == copied_match.game_state
        assert original_match.winner == copied_match.winner
        assert original_match.previous_player_who_played == copied_match.previous_player_who_played
        assert original_match.moves_played == copied_match.moves_played
        assert original_match.log == copied_match.log
        
        # Modify the copied match and check that the original match is not affected
        copied_match.make_move(2, "Player2")
        assert not np.array_equal(original_match.board, copied_match.board)
        assert original_match.moves_played != copied_match.moves_played
        assert original_match.log != copied_match.log

    def test_eq(self):
        match1 = ConnectXMatch(7, 6, 4, "Player1", "Player2")
        match2 = ConnectXMatch(7, 6, 4, "Player1", "Player2")
        assert match1 == match2

        match1.make_move(0, "Player1")
        assert match1 != match2

        match2.make_move(0, "Player1")
        assert match1 == match2

    def test_copy(self):
        original_match = ConnectXMatch(7, 6, 4, "Player1", "Player2")
        original_match.make_move(0, "Player1")
        copied_match = original_match.copy()

        assert original_match == copied_match

        copied_match.make_move(1, "Player2")
        assert original_match != copied_match

    def test_get_legal_actions(self, game: ConnectXMatch):
        game: ConnectXMatch = ConnectXMatch(columns=7, rows=1, win_length=4, first_player_name="X", second_player_name="O")
        # Initially, all columns should be legal actions
        assert game.getPossibleActions() == list(range(game.COLUMNS))

        # Fill up a column and check if it's removed from legal actions
        # Have to alternate 
        game.make_move(0, 'X')
        assert 0 not in game.getPossibleActions()

        # Ensure other columns are still legal
        assert set(game.getPossibleActions()) == set(range(1, game.COLUMNS))

        # Fill up all columns and check if no legal actions remain
        game.make_move(1, 'O')
        game.make_move(2, 'X')
        game.make_move(3, 'O')
        game.make_move(4, 'X')
        game.make_move(5, 'O')
        game.make_move(6, 'X')
        assert game.getPossibleActions() == []

def agent_first_column(board, win_length, opponent_name):
    # Simple agent that always picks the first available column
    return 0
def agent_last_column(board, win_length, opponent_name):
    # Simple agent that always picks the last available column
    return board.shape[0] - 1
        
def agent_empty(board, win_length, opponent_name):
    # Finds the first empty column and plays there
    # Otherwise random
    for col in range(1, board.shape[0]):
        if board[col][0] is None:
            return col
        elif board[col][1] == None:
            return col
        elif board[col][2] == None:
            return col
    return random.randint(0, board.shape[0] - 1)

def random_agent_1(board, win_length, opponent_name):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def random_agent_2(board, win_length, opponent_name):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

# Agent that raises an error after playing 2 moves
def delayed_error_agent(board, win_length, opponent_name):
    # Count how many pieces this agent has on the board
    pieces_count = 0
    for col in range(board.shape[0]):
        for row in range(board.shape[1]):
            if board[col][row] == "error_agent":
                pieces_count += 1
    
    # Raise an error after playing 2 moves
    if pieces_count >= 2:
        raise ValueError("This agent fails after playing 2 moves!")
    
    # Otherwise play in first available column
    for col in range(board.shape[0]):
        if board[col][0] is None:
            return col
    return 0

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
        
    def test_agents_receive_final_state(self):
        """Test that agents receive the final state after the game is finished."""
        # Create counters to track how many times each agent is called
        first_agent_calls = [0]
        second_agent_calls = [0]
        
        # Create custom agents that count their calls
        def first_agent_func(board, win_length, opponent_name):
            first_agent_calls[0] += 1
            return 0  # Always play first column
            
        def second_agent_func(board, win_length, opponent_name):
            second_agent_calls[0] += 1
            return board.shape[0] - 1  # Always play last column
        
        # Create a match with our custom agents
        match = ConnectXMatchWithAgents(
            7,  # columns
            6,  # rows
            4,  # win length
            "Player1",
            "Player2",
            first_agent_func,
            second_agent_func,
            5,  # time limit
            True  # enable thread protection
        )
        
        # Record initial call counts
        initial_first_calls = first_agent_calls[0]
        initial_second_calls = second_agent_calls[0]
        
        # Play the game - first agent should win after 4 moves
        winner = match.play_full_game()
        
        # Verify the winner
        assert winner == "Player1"
        
        # Agents should be called during gameplay, plus one extra time each for the final state
        # For a win after 4 columns, we expect 4 total moves (2 per player) plus the final state call
        game_play_calls = first_agent_calls[0] - initial_first_calls
        assert game_play_calls >= 3  # At least 2 for gameplay + 1 for final state
        
        game_play_calls = second_agent_calls[0] - initial_second_calls
        assert game_play_calls >= 3  # At least 2 for gameplay + 1 for final state
        
        # Test with agents that raise exceptions when called with final state
        def first_agent_error_func(board, win_length, opponent_name):
            if match.game.game_state != GameState.IN_PROGRESS:
                raise ValueError("Game already over!")
            return 0
            
        def second_agent_error_func(board, win_length, opponent_name):
            if match.game.game_state != GameState.IN_PROGRESS:
                raise ValueError("Game already over!")
            return board.shape[0] - 1
        
        # Create a new match with agents that raise errors on final state
        error_match = ConnectXMatchWithAgents(
            7, 6, 4, 
            "ErrorPlayer1", "ErrorPlayer2",
            first_agent_error_func, second_agent_error_func,
            5, True
        )
        
        # The game should still complete successfully despite the errors in final state calls
        winner = error_match.play_full_game()
        assert winner == "ErrorPlayer2"  # Game should still finish normally

    def test_error_handling(self):
        """Test that agent errors are properly handled during gameplay."""
        
        # Create an agent function that raises an exception
        def error_agent(board, win_length, opponent_name):
            raise ValueError("This agent always fails!")
            
        # Create a match with the error agent as first player
        match = ConnectXMatchWithAgents(
            7, 6, 4,
            "ErrorPlayer", "NormalPlayer",
            error_agent, agent_last_column,
            5, True
        )
        
        # The first move should fail and end the game
        result = match.play_move_with_agent("ErrorPlayer")
        
        # Verify that the game ended with an agent error
        assert result is False
        assert match.game.game_state == GameState.AGENT_ERROR
        assert match.game.winner == "NormalPlayer"
        assert match.game.previous_player_who_played == "ErrorPlayer"
        
        # Check that the log contains an error message
        assert any("caused an error" in log_entry for log_entry in match.game.log)
        
        # Test with thread protection disabled
        match = ConnectXMatchWithAgents(
            7, 6, 4,
            "ErrorPlayer", "NormalPlayer",
            error_agent, agent_last_column,
            5, False  # Disable thread protection
        )
        
        # The move should still fail
        result = match.play_move_with_agent("ErrorPlayer")
        assert result is False
        assert match.game.game_state == GameState.AGENT_ERROR
        
        # Test error handling in full game
        match = ConnectXMatchWithAgents(
            7, 6, 4,
            "ErrorPlayer", "NormalPlayer",
            error_agent, agent_last_column,
            5, True
        )
        
        # The game should end with the normal player winning
        winner = match.play_full_game()
        assert winner == "NormalPlayer"
        assert match.game.game_state == GameState.AGENT_ERROR

    def test_error_handling_in_matchup(self):
        """Test that agent errors are properly handled during matchup gameplay."""
        board_dim = BoardDimension(7, 6)
        
        # Create an agent that raises an error after a few moves
        def delayed_error_agent(board, win_length, opponent_name):
            # Count how many pieces this agent has on the board
            pieces_count = 0
            for col in range(board.shape[0]):
                for row in range(board.shape[1]):
                    if board[col][row] == "error_agent":
                        pieces_count += 1
            
            # Raise an error after playing 2 moves
            if pieces_count >= 2:
                raise ValueError("This agent fails after playing 2 moves!")
            
            # Otherwise play in first available column
            for col in range(board.shape[0]):
                if board[col][0] is None:
                    return col
            return 0
        
        # Create agents for testing
        error_agent = Agent("error_agent", delayed_error_agent)
        normal_agent = Agent("normal_agent", agent_last_column)
        
        # Create matchup
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,  # time limit
            10,  # win threshold
            True  # enable thread protection
        )
        
        # Play games sequentially instead of in parallel
        matchup.play_n_games(5)
        
        # Normal agent should win due to error_agent failing
        assert matchup.first_player_wins < 5
        assert matchup.second_player_wins > 0
        
        # Check that some games are saved and have proper error state
        if len(matchup.saved_player_2_games) > 0:
            for game in matchup.saved_player_2_games:
                if game.game_state == GameState.AGENT_ERROR:
                    assert game.winner == "normal_agent"
                    assert any("caused an error" in log_entry for log_entry in game.log)
                    
        # Test with thread protection disabled
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,
            10,
            False  # disable thread protection
        )
        
        # Play games sequentially
        matchup.play_n_games(5)
        
        # Normal agent should win some games due to error_agent failing
        assert matchup.second_player_wins > 0
        
        # Check if any games with AGENT_ERROR state were saved
        agent_error_games = 0
        for game in matchup.saved_player_2_games:
            if game.game_state == GameState.AGENT_ERROR:
                agent_error_games += 1
                assert game.winner == "normal_agent"
                assert any("caused an error" in log_entry for log_entry in game.log)
                
        # We should have at least one game with agent error
        assert agent_error_games > 0

    def test_generate_report(self):
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_last_column)
        matchup: Matchup = Matchup(
            board_dim,
            4,
            agent_1,
            agent_2,
            5,
            10
        )
        # Play the matchup
        matchup.play_n_games(10)
        # Generate the report
        matchup.generate_report("test_report.txt")      
        # Check that the report exists
        try:
            with open("test_report.txt", "r") as f:
                pass
        except FileNotFoundError:
            assert False
        # Remove the report
        os.remove("test_report.txt")






class TestMetaMatchup:
    def test_play_matchups(self):
        board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
        win_lengths = [4, 5]
        first_agent = Agent("Agent1", agent_first_column)
        second_agent = Agent("Agent2", agent_last_column)
        meta_matchup: MetaMatchup = MetaMatchup(
            board_dimensions,
            win_lengths,
            first_agent,
            second_agent,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Before playing matchups
        assert meta_matchup.matchups == []
        assert meta_matchup.overall_total_games == 0
        assert meta_matchup.overall_first_player_wins == 0
        assert meta_matchup.overall_second_player_wins == 0
        assert meta_matchup.overall_draws == 0
        assert meta_matchup.overall_percentage_first_player_wins is None
        assert meta_matchup.overall_percentage_second_player_wins is None
        assert meta_matchup.overall_percentage_draws is None
        assert meta_matchup.overall_winner is None
        # Play matchups
        meta_matchup.play_matchups()
        # After playing matchups
        assert len(meta_matchup.matchups) == len(board_dimensions) * len(win_lengths)
        assert meta_matchup.overall_total_games == len(board_dimensions) * len(win_lengths) * 10
        assert meta_matchup.overall_first_player_wins + meta_matchup.overall_second_player_wins + meta_matchup.overall_draws == meta_matchup.overall_total_games
        assert meta_matchup.overall_percentage_first_player_wins == 50.0
        assert meta_matchup.overall_percentage_second_player_wins == 50.0
        assert meta_matchup.overall_percentage_draws == 0.0
        assert meta_matchup.overall_winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'
        matchup_1: Matchup = meta_matchup.matchups[0]
        assert matchup_1.rows == board_dimensions[0].rows
        assert matchup_1.columns == board_dimensions[0].columns
        matchup_2: Matchup = meta_matchup.matchups[1]
        assert matchup_2.rows == board_dimensions[0].rows
        assert matchup_2.columns == board_dimensions[0].columns
        matchup_3: Matchup = meta_matchup.matchups[2]
        assert matchup_3.rows == board_dimensions[1].rows
        assert matchup_3.columns == board_dimensions[1].columns
        matchup_4: Matchup = meta_matchup.matchups[3]
        assert matchup_4.rows == board_dimensions[1].rows
        assert matchup_4.columns == board_dimensions[1].columns

        # Play matchups with a clear winner
        first_agent = Agent("Agent1", agent_first_column)
        second_agent = Agent("Agent2", agent_empty)
        meta_matchup: MetaMatchup = MetaMatchup(
            board_dimensions,
            win_lengths,
            first_agent,
            second_agent,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Play matchups
        meta_matchup.play_matchups()
        # After playing matchups
        assert len(meta_matchup.matchups) == len(board_dimensions) * len(win_lengths)
        assert meta_matchup.overall_total_games == len(board_dimensions) * len(win_lengths) * 10
        assert meta_matchup.overall_first_player_wins + meta_matchup.overall_second_player_wins + meta_matchup.overall_draws == meta_matchup.overall_total_games
        assert meta_matchup.overall_percentage_first_player_wins == 100.0
        assert meta_matchup.overall_percentage_second_player_wins == 0.0
        assert meta_matchup.overall_percentage_draws == 0.0
        assert meta_matchup.overall_winner == 'Agent1'

    def test_play_parallel_matchups(self):
        board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
        win_lengths = [4, 5]
        first_agent = Agent("Agent1", agent_first_column)
        second_agent = Agent("Agent2", agent_last_column)
        meta_matchup: MetaMatchup = MetaMatchup(
            board_dimensions,
            win_lengths,
            first_agent,
            second_agent,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Before playing matchups
        assert meta_matchup.matchups == []
        assert meta_matchup.overall_total_games == 0
        assert meta_matchup.overall_first_player_wins == 0
        assert meta_matchup.overall_second_player_wins == 0
        assert meta_matchup.overall_draws == 0
        assert meta_matchup.overall_percentage_first_player_wins is None
        assert meta_matchup.overall_percentage_second_player_wins is None
        assert meta_matchup.overall_percentage_draws is None
        assert meta_matchup.overall_winner is None
        # Play matchups
        meta_matchup.play_matchups()
        # After playing matchups
        assert len(meta_matchup.matchups) == len(board_dimensions) * len(win_lengths)
        assert meta_matchup.overall_total_games == len(board_dimensions) * len(win_lengths) * 10
        assert meta_matchup.overall_first_player_wins + meta_matchup.overall_second_player_wins + meta_matchup.overall_draws == meta_matchup.overall_total_games
        assert meta_matchup.overall_percentage_first_player_wins == 50.0
        assert meta_matchup.overall_percentage_second_player_wins == 50.0
        assert meta_matchup.overall_percentage_draws == 0.0
        assert meta_matchup.overall_winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'
        matchup_1: Matchup = meta_matchup.matchups[0]
        assert matchup_1.rows == board_dimensions[0].rows
        assert matchup_1.columns == board_dimensions[0].columns
        matchup_2: Matchup = meta_matchup.matchups[1]
        assert matchup_2.rows == board_dimensions[0].rows
        assert matchup_2.columns == board_dimensions[0].columns
        matchup_3: Matchup = meta_matchup.matchups[2]
        assert matchup_3.rows == board_dimensions[1].rows
        assert matchup_3.columns == board_dimensions[1].columns
        matchup_4: Matchup = meta_matchup.matchups[3]
        assert matchup_4.rows == board_dimensions[1].rows
        assert matchup_4.columns == board_dimensions[1].columns

        # Play matchups with a clear winner
        first_agent = Agent("Agent1", agent_first_column)
        second_agent = Agent("Agent2", agent_empty)
        meta_matchup: MetaMatchup = MetaMatchup(
            board_dimensions,
            win_lengths,
            first_agent,
            second_agent,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Play matchups
        meta_matchup.play_matchups()
        # After playing matchups
        assert len(meta_matchup.matchups) == len(board_dimensions) * len(win_lengths)
        assert meta_matchup.overall_total_games == len(board_dimensions) * len(win_lengths) * 10
        assert meta_matchup.overall_first_player_wins + meta_matchup.overall_second_player_wins + meta_matchup.overall_draws == meta_matchup.overall_total_games
        assert meta_matchup.overall_percentage_first_player_wins == 100.0
        assert meta_matchup.overall_percentage_second_player_wins == 0.0
        assert meta_matchup.overall_percentage_draws == 0.0
        assert meta_matchup.overall_winner == 'Agent1'

    def test_generate_report(self):
        board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
        win_lengths = [4, 5]
        first_agent = Agent("Agent1", agent_first_column)
        second_agent = Agent("Agent2", agent_last_column)
        meta_matchup: MetaMatchup = MetaMatchup(
            board_dimensions,
            win_lengths,
            first_agent,
            second_agent,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Play matchups
        meta_matchup.play_matchups()
        # Generate the report
        meta_matchup.generate_report("test_report.txt")      
        # Check that the report exists
        try:
            with open("test_report.txt", "r") as f:
                pass
        except FileNotFoundError:
            assert False
        # Remove the report
        os.remove("test_report.txt")






class TestTournament:
    def test_play_tournament(self):
        board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
        win_lengths = [4, 5]
        agents = [
            Agent("Agent1", agent_first_column),
            Agent("Agent2", agent_last_column),
            Agent("Agent3", agent_empty)
        ]
        tournament: Tournament = Tournament(
            board_dimensions,
            win_lengths,
            agents,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        
        # Before playing tournament
        assert tournament.meta_matchups == []
        assert tournament.overall_winner is None
        for agent in agents:
            assert tournament.agents_metamatchup_wins[agent.name] == 0
        
        # Play tournament
        tournament.play_tournament()
        
        # After playing tournament
        assert len(tournament.meta_matchups) == len(agents) * (len(agents) - 1) // 2
        assert tournament.overall_winner is not None
        total_wins = sum(tournament.agents_metamatchup_wins[agent.name] for agent in agents)
        assert total_wins == 2
        assert len(tournament.meta_matchups) == 3
        assert tournament.overall_winner == 'NO_CLEAR_WINNER'

    def test_generate_report(self):
        board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
        win_lengths = [4, 5]
        agents = [
            Agent("Agent1", agent_first_column),
            Agent("Agent2", agent_last_column),
            Agent("Agent3", agent_empty)
        ]
        tournament: Tournament = Tournament(
            board_dimensions,
            win_lengths,
            agents,
            turn_time_limit_s=5,
            win_percentage_threshold_for_win=10,
            number_of_games_per_matchup=10
        )
        # Play tournament
        tournament.play_tournament()
        # Create the directory if it does not exist
        if not os.path.exists("test_dir_for_tournament_reports"):
            os.mkdir("test_dir_for_tournament_reports")
        # Generate the reports
        tournament.generate_reports_in_dir("test_dir_for_tournament_reports")      
        # Check that the reports exists
        # Check that there is 4 reports in the directory
        reports = os.listdir("test_dir_for_tournament_reports")
        assert len(reports) == 4
        # Check that one of the reports is the overall report
        assert "tournament_result.txt" in reports
        # Remove the reports
        for report in reports:
            os.remove(f"test_dir_for_tournament_reports/{report}")
        # Remove the dir too
        os.rmdir("test_dir_for_tournament_reports")


class TestConnectXVisual:
    pass
    # def test_manual_start(self):
    #     visual = ConnectXVisual(7, 6, 4)
    #     visual.play_manual_game("X", "O")

    # def test_play_real_time_game(self):
    #     visual = ConnectXVisual(7, 6, 4)
    #     visual.play_real_time_game("X", "O", agent_first_column, agent_last_column, 100, 1)

    # def test_play_manual_against_agent(self):
    #     visual = ConnectXVisual(7, 6, 4)
    #     visual.play_manual_against_agent("Human", "AI", agent_first_column, True, 100, 0.2)

    # def test_play_multiple_real_time_games(self):
    #     visual = ConnectXVisual(7, 6, 4)
    #     agent_1: Agent = Agent("Agent1", agent_first_column)
    #     agent_2: Agent = Agent("Agent2", agent_last_column)
    #     visual.play_multiple_real_time_games(agent_1, agent_2, 1, 3, 10)

class TestConnectXMatchup:
    def test_play_matchup(self):
        ### Player 1 wins
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_empty)
        matchup: Matchup = Matchup(
            board_dim,
            4,
            agent_1,
            agent_2,
            5,
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
        matchup.play_n_games(10)
        # After
        assert matchup.first_player_wins == 10
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 100.0
        assert matchup.percentage_second_player_wins == 0.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner == "agent_1"

        ### Equal strats
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_last_column)
        matchup: Matchup = Matchup(
            board_dim,
            4,
            agent_1,
            agent_2,
            5,
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
        matchup.play_n_games(10)
        # After
        assert matchup.first_player_wins == 5
        assert matchup.second_player_wins == 5
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 50.0
        assert matchup.percentage_second_player_wins == 50.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'

    def test_play_single_game(self):
        """Test the _play_single_game static method."""
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_empty)
        win_length = 4
        time_limit = 5
        
        # Test first agent starting
        winner, game = Matchup._play_single_game(
            game_index=0,
            board_dimension=board_dim,
            win_length=win_length,
            first_agent=agent_1,
            second_agent=agent_2,
            time_limit=time_limit,
            enable_thread_protection=True,
            start_with_first_agent=True
        )
        
        # agent_1 (agent_first_column) should win consistently
        assert winner == "agent_1"
        assert game.winner == "agent_1"
        assert game.FIRST_PLAYER_NAME == "agent_1"
        assert game.SECOND_PLAYER_NAME == "agent_2"
        
        # Test second agent starting
        winner, game = Matchup._play_single_game(
            game_index=1,
            board_dimension=board_dim,
            win_length=win_length,
            first_agent=agent_1,
            second_agent=agent_2,
            time_limit=time_limit,
            enable_thread_protection=True,
            start_with_first_agent=False
        )
        
        # agent_1 should still win but will be the second player this time
        assert winner == "agent_1"
        assert game.winner == "agent_1"
        assert game.FIRST_PLAYER_NAME == "agent_2"
        assert game.SECOND_PLAYER_NAME == "agent_1"
        
        # Test with thread protection disabled
        winner, game = Matchup._play_single_game(
            game_index=2,
            board_dimension=board_dim,
            win_length=win_length,
            first_agent=agent_1,
            second_agent=agent_2,
            time_limit=time_limit,
            enable_thread_protection=False,
            start_with_first_agent=True
        )
        
        # Should still work without thread protection
        assert winner == "agent_1"
        assert game.winner == "agent_1"

    def test_play_n_games_with_parallelism(self):
        """Test the play_n_games_with_parallelism method."""
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_empty)
        matchup = Matchup(
            board_dim,
            4,
            agent_1,
            agent_2,
            5,
            10
        )
        
        # Before playing any games
        assert matchup.first_player_wins == 0
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        
        # Play 10 games in parallel
        matchup.play_n_games_with_parallelism(10, num_processes=2)
        
        # After playing games - agent_1 should win all of them (10 wins)
        assert matchup.first_player_wins == 10
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 100.0
        assert matchup.percentage_second_player_wins == 0.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner == "agent_1"
        
        # Verify game records are saved
        assert len(matchup.saved_player_1_games) == 5  # Maximum 5 games are saved
        assert len(matchup.saved_player_2_games) == 0
        
        # Play 5 more games - statistics should accumulate
        matchup.play_n_games_with_parallelism(5, num_processes=2)
        
        # Now we should have 15 wins for agent_1
        assert matchup.first_player_wins == 15
        assert matchup.second_player_wins == 0
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 100.0
        assert matchup.winner == "agent_1"
        
        # Test with equal strategies
        board_dim = BoardDimension(7, 6)
        agent_1 = Agent("agent_1", agent_first_column)
        agent_2 = Agent("agent_2", agent_last_column)
        matchup = Matchup(
            board_dim,
            4,
            agent_1,
            agent_2,
            5,
            10
        )
        
        # Play 10 games in parallel
        matchup.play_n_games_with_parallelism(10, num_processes=2)
        
        # Agents should have roughly equal wins
        assert matchup.first_player_wins == 5
        assert matchup.second_player_wins == 5
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 50.0
        assert matchup.percentage_second_player_wins == 50.0
        assert matchup.percentage_draws == 0.0
        assert matchup.winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'
        
        # Play 10 more games - statistics should accumulate and not be reset
        matchup.play_n_games_with_parallelism(10, num_processes=2)
        
        # Now we should have 20 games total
        total_games = matchup.first_player_wins + matchup.second_player_wins + matchup.draws
        assert total_games == 20
        # Roughly 50/50 win split
        assert abs(matchup.first_player_wins - matchup.second_player_wins) <= 2
        assert matchup.winner == 'NO CLEAR WINNER. The difference in win percentage is less than the threshold.'
        
    def test_error_handling_in_matchup(self):
        """Test that agent errors are properly handled during matchup gameplay."""
        # Define a counter to track when to raise an error
        error_counter = [0]
        
        # Create an agent that fails after a specific number of calls
        def count_and_fail_agent(board, win_length, opponent_name):
            error_counter[0] += 1
            # Fail on the third call
            if error_counter[0] >= 3:
                raise ValueError("This agent fails after being called 3 times!")
            return 0  # Always play in first column
            
        board_dim = BoardDimension(7, 6)
        error_agent = Agent("error_agent", count_and_fail_agent)
        normal_agent = Agent("normal_agent", agent_last_column)
        
        # Create matchup
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,  # time limit
            10,  # win threshold
            True  # enable thread protection
        )
        
        # Play games sequentially instead of in parallel
        matchup.play_n_games(5)
        
        # Normal agent should win due to error_agent failing
        assert matchup.first_player_wins < 5
        assert matchup.second_player_wins > 0
        
        # Check that some games are saved and have proper error state
        if len(matchup.saved_player_2_games) > 0:
            for game in matchup.saved_player_2_games:
                if game.game_state == GameState.AGENT_ERROR:
                    assert game.winner == "normal_agent"
                    assert any("caused an error" in log_entry for log_entry in game.log)
                    
        # Test with thread protection disabled
        error_counter[0] = 0  # Reset the counter
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,
            10,
            False  # disable thread protection
        )
        
        # Play games sequentially
        matchup.play_n_games(5)
        
        # Normal agent should win some games due to error_agent failing
        assert matchup.second_player_wins > 0
        
        # Check if any games with AGENT_ERROR state were saved
        agent_error_games = 0
        for game in matchup.saved_player_2_games:
            if game.game_state == GameState.AGENT_ERROR:
                agent_error_games += 1
                assert game.winner == "normal_agent"
                assert any("caused an error" in log_entry for log_entry in game.log)
                
        # We should have at least one game with agent error
        assert agent_error_games > 0

    def test_error_handling_in_parallel_gameplay(self):
        """Test that agent errors are properly handled during parallel gameplay."""
        board_dim = BoardDimension(7, 6)
        
        # Create agents for testing - using the global delayed_error_agent function
        error_agent = Agent("error_agent", delayed_error_agent)
        normal_agent = Agent("normal_agent", agent_last_column)
        
        # Create matchup
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,
            10,
            True  # enable thread protection
        )
        
        # Play games in parallel
        matchup.play_n_games_with_parallelism(10, num_processes=2)
        
        # Normal agent should win all games due to error_agent failing
        assert matchup.first_player_wins == 0
        assert matchup.second_player_wins == 10
        assert matchup.draws == 0
        assert matchup.percentage_first_player_wins == 0.0
        assert matchup.percentage_second_player_wins == 100.0
        assert matchup.winner == "normal_agent"
        
        # Check that some games are saved
        assert len(matchup.saved_player_1_games) == 0
        assert len(matchup.saved_player_2_games) > 0
        
        # Verify that error messages are in the game logs
        for game in matchup.saved_player_2_games:
            assert any("caused an error" in log_entry for log_entry in game.log)
            assert game.game_state == GameState.AGENT_ERROR
            assert game.winner == "normal_agent"
            
        # Test with thread protection disabled
        matchup = Matchup(
            board_dim,
            4,
            error_agent,
            normal_agent,
            5,
            10,
            False  # disable thread protection
        )
        
        # Play games in parallel
        matchup.play_n_games_with_parallelism(10, num_processes=2)
        
        # Results should be the same without thread protection
        assert matchup.first_player_wins == 0
        assert matchup.second_player_wins == 10
        assert matchup.draws == 0
        assert matchup.winner == "normal_agent"

if __name__ == "__main__":
    unittest.main()
