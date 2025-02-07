import unittest
import tkinter as tk
from main.connect import ConnectTesta, Connect




import pytest
from main.connect import Connect, ConnectTesta
import tkinter as tk
import random

@pytest.fixture
def game():
    return Connect(columns=7, rows=6, win_length=4)

def test_horizontal_win(game):
    # Simulate a horizontal win
    for col in range(4):
        assert not game.check_win()
        game.make_move(col, 'X')
    assert game.check_win()

def test_vertical_win(game):
    # Simulate a vertical win
    for row in range(4):
        assert not game.check_win()
        game.make_move(0, 'X')
    assert game.check_win()

def test_diagonal_win(game):
    # Simulate a diagonal win
    for i in range(4):
        assert not game.check_win()
        for j in range(i):
            game.make_move(i, 'O')
        game.make_move(i, 'X')
    assert game.check_win()

def test_anti_diagonal_win(game):
    # Simulate an anti-diagonal win
    for i in range(4):
        for j in range(3 - i):
            game.make_move(i, 'O')
        game.make_move(i, 'X')
    assert game.check_win()

def test_no_win(game):
    # Ensure no win is detected when there is no win
    game.make_move(0, 'X')
    game.make_move(1, 'X')
    game.make_move(2, 'X')
    assert not game.check_win()

def test_corner_win(game):
    ## Bottom left corner
    # Simulate columns win in the bottom-left corner
    for row in range(4):
        game.make_move(0, 'X')
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the bottom-left corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.make_move(col, 'X')
        if col < 3:
            assert not game.check_win()
    assert game.check_win()

    ## Bottom right corner
    # Simulate columns win in the bottom-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for row in range(4):
        game.make_move(game.columns - 1, 'X')
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the bottom-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.make_move(game.columns - 1 - col, 'X')
        if col < 3:
            assert not game.check_win()
    assert game.check_win()

    ## Top left corner
    # Simulate columns win in the top-left corner
    game = Connect(columns=7, rows=6, win_length=4)
    for row in range(4):
        game.board[0][-1-row] = 'X'
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the top-left corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.board[col][-1] = 'X'
        if col < 3:
            assert not game.check_win()
    assert game.check_win()

    ## Top right corner
    # Simulate columns win in the top-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for row in range(4):
        game.board[-1][-1-row] = 'X'
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the top-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.board[-1-col][-1] = 'X'
        if col < 3:
            assert not game.check_win()
    assert game.check_win()

def agent_1(board, win_length):
    # Simple agent that always picks the first available column
    for col in range(board.shape[0]):
        if board[col][0] is None:
            return col

def agent_2(board, win_length):
    # Simple agent that always picks the last available column
    for col in range(board.shape[0] - 1, -1, -1):
        if board[col][0] is None:
            return col

def random_agent_1(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def random_agent_2(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def test_play_game():
    test = ConnectTesta("Agent 1", agent_1, "Agent 2", agent_2)
    test.play_game_with_visual(columns=7, rows=6, win_length=4, starter="Agent 1")

def test_play_automatic_game():
    test = ConnectTesta("Random Agent 1", random_agent_1, "Random Agent 2", random_agent_2)
    test.play_automatic_game_with_visual(columns=7, rows=6, win_length=4, starter="Random Agent 1", seconds_between_moves=1)

def agent_1_func(board, win_length):
    # Simple agent that always plays the first available column
    for col in range(len(board)):
        if board[col][0] is None:
            return col
    return 0

def agent_2_func(board, win_length):
    # Simple agent that always plays the last available column
    for col in reversed(range(len(board))):
        if board[col][0] is None:
            return col
    return len(board) - 1

class TestConnectX(unittest.TestCase):
    def test_play_step_game_with_visual(self):
        game_tester = ConnectTesta("Agent 1", agent_1_func, "Agent 2", agent_2_func)
        columns, rows, win_length = 7, 6, 4
        starter = "Agent 1"
        
        # Create a root window for the test
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Run the game with visual step-by-step play
        game_tester.play_step_game_with_visual(columns, rows, win_length, starter)
        
        # Check if the game window is created
        self.assertTrue(isinstance(game_tester, ConnectTesta))
        
        # Close the root window after the test
        root.destroy()

    def test_draw_condition(self):
        game_tester = ConnectTesta("Agent 1", agent_1_func, "Agent 2", agent_2_func)
        columns, rows, win_length = 7, 6, 10
        starter = "Agent 1"
        
        game = Connect(columns, rows, win_length)
        
        # Fill the board without any player winning
        for col in range(columns):
            for row in range(rows):
                player = "Agent 1" if (col + row) % 2 == 0 else "Agent 2"
                game.make_move(col, player)
        
        # Check if the game is a draw
        with self.assertRaises(Exception) as context:
            game.check_win()
        
        self.assertTrue("The game is a draw. All columns are full." in str(context.exception))

if __name__ == "__main__":
    unittest.main()
