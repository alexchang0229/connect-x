import numpy as np

class Connect:
    def __init__(self, columns: int, rows: int, win_length: int):
        self.board = np.full((columns, rows), None)
        self.columns = columns
        self.rows = rows
        self.win_length = win_length
        self.current_player = 1  # Start with player 1

    def make_move(self, column: int) -> bool:
        if column < 0 or column >= self.columns:
            return False
        for row in range(self.rows):
            if self.board[row][column] is None:
                self.board[row][column] = self.current_player
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
            
    def check_win_2(self) -> bool:
        # temp_board= np.pad(self.board, pad_width=self.win_length, mode='constant', constant_values=Player.EMPTY)
        # new_x = x + self.win_length
        # new_y = y + self.win_length
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] is not None:
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
        self.current_player = 1 if self.current_player == 0 else 0

    @staticmethod
    def beautify_transformation(val):
        if val == 1:
            return "P_1"
        elif val == 0:
            return "P_2"
        else:
            return "EMPTY"

    def __str__(self):
        vectorized_transform = np.vectorize(self.beautify_transformation)
        arr = vectorized_transform(self.board)
        return str(arr)
    
# def play(game: np.Array) -> int:
#     game.board[0, 0] -> 1, 0, None