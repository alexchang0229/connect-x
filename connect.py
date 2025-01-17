import numpy as np
from enum import Enum

class Player(str, Enum):
    PLAYER_1 = "PLAYER_1"
    PLAYER_2 = "PLAYER_2"
    EMPTY = "EMPTY"

class Jetton:
    def __init__(self, owner: str):
        self.owner = owner

class Board:
    def __init__(self, rows: int, columns: int):
        self.board = np.full((rows, columns), Player.EMPTY)

    @staticmethod
    def beautify_transformation(val):
        if val == Player.PLAYER_1:
            return "P_1"
        elif val == Player.PLAYER_2:
            return "P_2"
        else:
            return "EMPTY"


    def __str__(self):
        vectorized_transform = np.vectorize(Board.beautify_transformation)
        arr = vectorized_transform(self.board)
        return str(arr)
