import numpy as np
import itertools
import tkinter as tk

from typing import Callable

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
        if all(all(self.board[col][row] is not None for row in range(self.rows)) for col in range(self.columns)):
            raise Exception("The game is a draw. All columns are full.")
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

class ConnectXVisual:
    def __init__(self, game: Connect, agent_1_name: str, agent_2_name: str):
        self.game = game
        self.agent_1_name = agent_1_name
        self.agent_2_name = agent_2_name
        self.player = agent_1_name
        self.width = 100
        self.height = 100
        self.game_over = False

    def update_board(self):
        for col in range(self.game.columns):
            for row in range(self.game.rows):
                value = self.game.board[col][row]
                color = "white" if value is None else ("red" if value == self.agent_1_name else "yellow")
                canvas = self.cells[col][row]
                canvas.delete("all")
                if value is not None:
                    canvas.create_oval(5, 5, self.width-5, self.height-5, fill=color)
                    canvas.create_text(self.width/2, self.height/2, text=value, fill="black")

    def make_move_and_update(self, column):
        if self.game_over:
            return
        try:
            self.game.make_move(column, self.player)
            self.update_board()
            if self.game.check_win():
                winner_color = "red" if self.player == self.agent_1_name else "yellow"
                self.result_label.config(text=f"{self.player} wins!", font=("Helvetica", 24), fg=winner_color)
                for col in range(self.game.columns):
                    for row in range(self.game.rows):
                        self.cells[col][row].config(bg="light green")
                self.game_over = True
                for button in self.buttons:
                    button.config(state=tk.DISABLED)
                return
            self.player = self.agent_1_name if self.player == self.agent_2_name else self.agent_2_name
        except Exception as e:
            self.result_label.config(text=str(e))
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)

    def setup(self):
        self.root = tk.Tk()
        self.root.title("Connect X")

        self.cells = [[tk.Canvas(self.root, width=100, height=100, bg="white", borderwidth=2, relief="groove") for _ in range(self.game.rows)] for _ in range(self.game.columns)]
        for col in range(self.game.columns):
            for row in range(self.game.rows):
                self.cells[col][row].grid(row=row, column=col)

        self.buttons = [tk.Button(self.root, text=f"Drop {col+1}", command=lambda col=col: self.make_move_and_update(col)) for col in range(self.game.columns)]
        for col, button in enumerate(self.buttons):
            button.grid(row=self.game.rows, column=col)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=self.game.rows+1, columnspan=self.game.columns)

    def manual_start(self):
        self.root.mainloop()

    def automatic_start(self, agent_1_func: Callable, agent_2_func: Callable, time_between_moves: int):
        def play_next_move():
            if self.game_over:
                return
            if self.player == self.agent_1_name:
                column = agent_1_func(self.game.board, self.game.win_length)
            else:
                column = agent_2_func(self.game.board, self.game.win_length)
            self.make_move_and_update(column)
            if not self.game_over:
                self.root.after(time_between_moves, play_next_move)

        self.setup()
        self.root.after(time_between_moves, play_next_move)
        self.root.mainloop()


class ConnectTesta:
    def __init__(self, agent_1_name: str, agent_1_func: Callable, agent_2_name: str, agent_2_func: Callable):
        self.agent_1_name: str = agent_1_name
        self.agent_1_func: Callable = agent_1_func
        self.agent_2_name: str = agent_2_name
        self.agent_2_func: Callable = agent_2_func
        
    def play_game(self, columns: int, rows: int, win_length: int, starter: str):
        game = Connect(columns, rows, win_length)
        player = starter
        while not game.check_win():
            if player == self.agent_1_name:
                column = self.agent_1_func(game.board, win_length)
            else:
                column = self.agent_2_func(game.board, win_length)
            game.make_move(column, player)
            player = self.agent_1_name if player == self.agent_2_name else self.agent_2_name
        return player
    
    def play_game_with_print(self, columns: int, rows: int, win_length: int, starter: str):
        game = Connect(columns, rows, win_length)
        player = starter
        while not game.check_win():
            print(game)
            if player == self.agent_1_name:
                column = self.agent_1_func(game.board, win_length)
            else:
                column = self.agent_2_func(game.board, win_length)
            game.make_move(column, player)
            player = self.agent_1_name if player == self.agent_2_name else self.agent_2_name
        print(game)
        return player
    
    def play_game_with_visual(self, columns: int, rows: int, win_length: int, starter: str):
        game = Connect(columns, rows, win_length)
        visual = ConnectXVisual(game, self.agent_1_name, self.agent_2_name)
        visual.setup()
        visual.manual_start()

    def play_automatic_game_with_visual(self, columns: int, rows: int, win_length: int, starter: str, seconds_between_moves: int):
        milliseconds_between_moves = seconds_between_moves * 1000
        game = Connect(columns, rows, win_length)
        visual = ConnectXVisual(game, self.agent_1_name, self.agent_2_name)
        visual.automatic_start(self.agent_1_func, self.agent_2_func, milliseconds_between_moves)
