import numpy as np
import itertools

class Connect:
    def __init__(self, columns: int, rows: int, win_length: int):
        self.board = np.full((columns, rows), None)
        self.columns = columns
        self.rows = rows
        self.win_length = win_length

    def make_move(self, column: int, player: str) -> bool:
        if column < 0 or column >= self.columns:
            raise Exception("Invalid column")
        for row in range(self.rows):
            if self.board[column][row] is None:
                self.board[column][row] = player
                return True
        raise Exception("Column is full")
    
    def check_win(self) -> bool:
        for x, y in itertools.product(range(self.columns), range(self.rows)):
            if self.check_win_at_position(x, y):
                return True
        return False
    
    def check_win_at_position(self, x, y) -> bool:
        # Make a subarray with lower left corner at x, y
        # First, check if enough space to the right and above
        num_columns_on_right = self.columns - x - 1
        num_rows_above = self.rows - y - 1
        if num_columns_on_right < self.win_length - 1 or num_rows_above < self.win_length - 1:
            return False
        else:
            # Get subarray
            subarray = self.board[x:x+self.win_length, y:y+self.win_length]
            # Check if there is a win in the subarray
            return self.check_subarray_win(subarray)
            
    def check_subarray_win(self, subarray: np.ndarray) -> bool:
        # Check columns
        for column in range(self.win_length):
            if subarray[column, 0] is None:
                continue
            if all(subarray[column, :] == subarray[column, 0]):
                return True
        # Check rows
        for row in range(self.win_length):
            if subarray[0, row] is None:
                continue
            if all(subarray[:, row] == subarray[0, row]):
                return True
        # Check diagonals
        if subarray[0, 0] is not None and all(subarray.diagonal() == subarray[0, 0]):
            return True
        if subarray[0, -1] is not None and all(np.fliplr(subarray).diagonal() == subarray[0, -1]):
            return True
        return False
            
    @staticmethod
    def beautify_transformation(val: str):
        if val is None:
            return "____"
        elif len(val) < 4:
            return val.ljust(4, ' ')
        else:
            return val[:4]

    def __str__(self):
        vectorized_transform = np.vectorize(self.beautify_transformation)
        arr = vectorized_transform(self.board)
        rotated_arr = np.rot90(arr)
        return str(rotated_arr)
