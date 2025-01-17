import pytest
from connect import Connect, Player

@pytest.fixture
def game():
    return Connect(columns=7, rows=6, win_length=4)

def test_check_win_horizontal(game):
    # Simulate a horizontal win for PLAYER_1
    for col in range(4):
        game.board[0][col] = Player.PLAYER_1
    assert game.check_win()

def test_check_win_vertical(game):
    # Simulate a vertical win for PLAYER_1
    for row in range(4):
        game.board[row][0] = Player.PLAYER_1
    assert game.check_win()

def test_check_win_diagonal_positive(game):
    # Simulate a positive diagonal win for PLAYER_1
    for i in range(4):
        game.board[i][i] = Player.PLAYER_1
    assert game.check_win()

def test_check_win_diagonal_negative(game):
    # Simulate a negative diagonal win for PLAYER_1
    for i in range(4):
        game.board[i][3 - i] = Player.PLAYER_1
    assert game.check_win()

def test_check_win_no_win(game):
    # Ensure no win is detected when there is no win
    game.board[0][0] = Player.PLAYER_1
    game.board[0][1] = Player.PLAYER_2
    game.board[0][2] = Player.PLAYER_1
    game.board[0][3] = Player.PLAYER_2
    assert not game.check_win()

def test_check_win_direction_horizontal(game):
    # Test horizontal win direction
    for col in range(4):
        game.board[0][col] = Player.PLAYER_1
    assert game.check_win_direction(0, 0, 1, 0)

def test_check_win_direction_vertical(game):
    # Test vertical win direction
    for row in range(4):
        game.board[row][0] = Player.PLAYER_1
    assert game.check_win_direction(0, 0, 0, 1)

def test_check_win_direction_diagonal_positive(game):
    # Test positive diagonal win direction
    for i in range(4):
        game.board[i][i] = Player.PLAYER_1
    assert game.check_win_direction(0, 0, 1, 1)

def test_check_win_direction_diagonal_negative(game):
    # Test negative diagonal win direction
    for i in range(4):
        game.board[i][3 - i] = Player.PLAYER_1
    assert game.check_win_direction(0, 3, 1, -1)

def test_check_win_direction_no_win(game):
    # Ensure no win is detected in a specific direction when there is no win
    game.board[0][0] = Player.PLAYER_1
    game.board[0][1] = Player.PLAYER_2
    assert not game.check_win_direction(0, 0, 1, 0)