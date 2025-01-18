import pytest
from connect import Connect

@pytest.fixture
def game():
    return Connect(columns=7, rows=6, win_length=4)

def test_horizontal_win(game):
    # Simulate a horizontal win
    for col in range(4):
        game.make_move(col, 'X')
    assert game.check_win()

def test_vertical_win(game):
    # Simulate a vertical win
    for row in range(4):
        game.make_move(0, 'X')
    assert game.check_win()

def test_diagonal_win(game):
    # Simulate a diagonal win
    for i in range(4):
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
        game.make_move(0, 'X')
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the top-left corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.make_move(col, 'X')
        if col < 3:
            assert not game.check_win()
    assert game.check_win()

    ## Top right corner
    # Simulate columns win in the top-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for row in range(4):
        game.make_move(game.columns - 1, 'X')
        if row < 3:
            assert not game.check_win()
    assert game.check_win()
    # Simulate row win in the top-right corner
    game = Connect(columns=7, rows=6, win_length=4)
    for col in range(4):
        game.make_move(game.columns - 1 - col, 'X')
        if col < 3:
            assert not game.check_win()
    assert game.check_win()