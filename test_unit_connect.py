from connect import *

def test_unit_print():
    board = Board(4, 3)
    s = str(board)
    assert "EMPTY" in s
    print(board)
    print("Hello")