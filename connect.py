import numpy as np
from enum import Enum

class Player(str, Enum):
    PLAYER_1 = "PLAYER_1"
    PLAYER_2 = "PLAYER_2"
    EMPTY = "EMPTY"

class Connect:
    def __init__(self, columns: int, rows: int, win_length: int):
        self.board = np.full((rows, columns), Player.EMPTY)
        self.rows = rows
        self.columns = columns
        self.win_length = win_length
        self.current_player = Player.PLAYER_1

    def make_move(self, column: int) -> bool:
        if column < 0 or column >= self.columns:
            return False

        for row in range(self.rows):
            if self.board[row][column] == Player.EMPTY:
                self.board[row][column] = self.current_player
                return True

        return False

    def check_win(self) -> bool:
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] != Player.EMPTY:
                    if self.check_win_direction(column, row, 1, 0):
                        return True
                    if self.check_win_direction(column, row, 0, 1):
                        return True
                    if self.check_win_direction(column, row, 1, 1):
                        return True
                    if self.check_win_direction(column, row, 1, -1):
                        return True

        return False

    def check_win_direction(self, column: int, row: int, delta_column: int, delta_row: int) -> bool:
        for i in range(1, self.win_length):
            new_row = row + i * delta_row
            new_column = column + i * delta_column

            if new_row < 0 or new_row >= self.rows or new_column < 0 or new_column >= self.columns:
                return False

            if self.board[new_row][new_column] != self.board[row][column]:
                return False

        return True

    def switch_player(self):
        if self.current_player == Player.PLAYER_1:
            self.current_player = Player.PLAYER_2
        else:
            self.current_player = Player.PLAYER_1

    @staticmethod
    def beautify_transformation(val):
        if val == Player.PLAYER_1:
            return "P_1"
        elif val == Player.PLAYER_2:
            return "P_2"
        else:
            return "EMPTY"

    def __str__(self):
        vectorized_transform = np.vectorize(beautify_transformation)
        arr = vectorized_transform(self.board)
        return str(arr)