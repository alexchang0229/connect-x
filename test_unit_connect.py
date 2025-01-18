import pytest
import numpy as np
from connect import Connect

@pytest.fixture
def game():
    return Connect(columns=7, rows=6, win_length=4)

def test_check_subarray_win_column(game):
    subarray = np.array([
        [1, 1, 1, 1],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ])
    assert game.check_subarray_win(subarray)

def test_check_subarray_win_row(game):
    subarray = np.array([
        [1, None, None, None],
        [1, None, None, None],
        [1, None, None, None],
        [1, None, None, None]
    ])
    assert game.check_subarray_win(subarray)

def test_check_subarray_win_diagonal(game):
    subarray = np.array([
        [1, None, None, None],
        [None, 1, None, None],
        [None, None, 1, None],
        [None, None, None, 1]
    ])
    assert game.check_subarray_win(subarray)

def test_check_subarray_win_anti_diagonal(game):
    subarray = np.array([
        [None, None, None, 1],
        [None, None, 1, None],
        [None, 1, None, None],
        [1, None, None, None]
    ])
    assert game.check_subarray_win(subarray)

def test_check_subarray_no_win(game):
    subarray = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, None, None, 0],
        [0, 1, 0, 1]
    ])
    assert not game.check_subarray_win(subarray)

# def test_unit_print():
#     board = Connect(4, 3)
#     s = str(board)
#     assert "EMPTY" in s
#     print(board)
#     print("Hello")