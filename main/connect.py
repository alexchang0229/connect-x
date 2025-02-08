import numpy as np
import itertools
import tkinter as tk
from enum import Enum
from typing import Tuple, List, Callable
import threading

from typing import Callable

class ConnectXMatch:
    class GameState(str, Enum):
        """
        Enum representing the possible states of a Connect X game.
        """
        DRAW = "DRAW"
        WIN = "WIN"
        IN_PROGRESS = "IN_PROGRESS"
        ILLEGAL_MOVE = "ILLEGAL_MOVE"
        TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"

    """
    This class represents a single Connect X game match.
    """
    def __init__(
        self, 
        columns: int, 
        rows: int, 
        win_length: int,
        first_player_name: str,
        second_player_name: str
    ):
        self.COLUMNS: int = columns
        self.ROWS: int = rows
        self.WIN_LENGTH: int = win_length
        self.FIRST_PLAYER_NAME: str = first_player_name
        self.SECOND_PLAYER_NAME: str = second_player_name

        self.board: np.ndarray = np.full((columns, rows), None)
        self.game_state: GameState = GameState.IN_PROGRESS
        self.winner: str = None
        self.previous_player_who_played: str = None
        self.moves_played: Tuple[str, int] = []
        self.log: List[str] = []

    def get_other_player(self, player: str) -> str:
        if player == self.FIRST_PLAYER_NAME:
            return self.SECOND_PLAYER_NAME
        return self.FIRST_PLAYER_NAME

    def check_illegal_move(self, column: int, player: str) -> Tuple[GameState, str]:
        # Check if player exists
        if player not in [self.FIRST_PLAYER_NAME, self.SECOND_PLAYER_NAME]:
            raise Exception(f"Error, player {player} is not in the game.")
        # Check if the game is in progress.
        if self.game_state != GameState.IN_PROGRESS:
            raise Exception(f"Error, tried to play while in terminal state. Cannot play in game state: {self.game_state}")
        # Check if the column is valid.
        if column < 0 or column >= self.COLUMNS:
            return GameState.ILLEGAL_MOVE
        # Check if the column is already full before move.
        for row in range(0, self.ROWS):
            if self.board[column][row] is None:
                return GameState.IN_PROGRESS, ""
        return GameState.ILLEGAL_MOVE, "Tried to play in a full column"
    
    def check_win(self) -> bool:
        for x, y in itertools.product(range(self.COLUMNS), range(self.ROWS)):
            if self.check_win_at_position(x, y):
                return True
        return False
    
    def check_win_at_position(self, x, y) -> bool:
        # Make a subarray with lower left corner at x, y
        # First, check if enough space to the right and above
        num_columns_on_right = self.COLUMNS - x - 1
        num_rows_above = self.ROWS - y - 1
        if num_columns_on_right < self.WIN_LENGTH - 1 or num_rows_above < self.WIN_LENGTH - 1:
            return False
        else:
            # Get subarray
            subarray = self.board[x:x+self.WIN_LENGTH, y:y+self.WIN_LENGTH]
            # Check if there is a win in the subarray
            return self.check_subarray_win(subarray)
            
    def check_subarray_win(self, subarray: np.ndarray) -> bool:
        # Check columns
        for column in range(self.WIN_LENGTH):
            if subarray[column, 0] is None:
                continue
            if all(subarray[column, :] == subarray[column, 0]):
                return True
        # Check rows
        for row in range(self.WIN_LENGTH):
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
    
    def check_draw(self) -> bool:
        if all(all(self.board[col][row] is not None for row in range(self.ROWS)) for col in range(self.COLUMNS)):
            return True
        return False
    
    def make_move(self, column: int, player: str) -> bool:
        """ This method:
            Checks for illegal moves.
            Updates the game board.
            Checks for wins and draws.
            Updates the game state.
            Updates the winner.
            Updates the last player to have played.
            Adds to the log.
            makes updates the game board with a move from a player.

        Args:
            column (int): The column in which to play the move.
            player (str): The player making the move.

        Returns:
            bool: True if the move was goes on, False otherwise.
        """
        # Add move to the list of moves
        self.moves_played.append((player, column))
        # Check if the move is illegal
        state, message = self.check_illegal_move(column, player)
        # UPDATE STATE FOR ILLEGAL MOVE
        if state == GameState.ILLEGAL_MOVE:
            # Update state
            self.game_state = state
            self.winner = self.previous_player_who_played
            self.previous_player_who_played = player
            self.log.append(message)
            self.log.append(f"Player {player} tried to play in full column {column} and lost.")
            print(message)
            return False
        # Make the actual move - modify the game board
        for row in range(0, self.ROWS):
            if self.board[column][row] is None:
                self.board[column][row] = player
        # UPDATE STATE FOR WIN
        if self.check_win():
            self.game_state = GameState.WIN
            self.winner = player
            self.previous_player_who_played = player
            self.log.append(f"Player {player} won the game.")
            return False
        # UPDATE STATE FOR DRAW
        if self.check_draw():
            self.game_state = GameState.DRAW
            self.previous_player_who_played = player
            self.log.append("The game is a draw. All columns are full.")
            return False
        # UPDATE STATE FOR IN PROGRESS
        self.log.append(f"Player {player} played in column {column}.")
        self.previous_player_who_played = player
        return True

    def play_with_next_player(self, column: int) -> GameState:
        """ Automatically figures out the next player to play based on the last player to have played.
        """
        # Determine the current player
        if self.previous_player_who_played is None:
            next_player = self.FIRST_PLAYER_NAME
        else:
            next_player = self.get_other_player(self.previous_player_who_played)
        return self.make_move(column, next_player)

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
                x = col
                y = self.game.rows - row - 1  # Invert the row index
                canvas = self.cells[x][y]
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

    def automatic_timed_start(self, agent_1_func: Callable, agent_2_func: Callable, time_between_moves: int):
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
        visual.automatic_timed_start(self.agent_1_func, self.agent_2_func, milliseconds_between_moves)

    def play_step_game_with_visual(self, columns: int, rows: int, win_length: int, starter: str):
        game = Connect(columns, rows, win_length)
        visual = ConnectXVisual(game, self.agent_1_name, self.agent_2_name)
        visual.setup()
        
        def play_next_move(event=None):
            if game.check_win():
                return
            player = self.agent_1_name if visual.player == self.agent_1_name else self.agent_2_name
            column = self.agent_1_func(game.board, win_length) if player == self.agent_1_name else self.agent_2_func(game.board, win_length)
            visual.make_move_and_update(column)
        
        continue_button = tk.Button(visual.root, text="Continue", command=play_next_move)
        continue_button.grid(row=game.rows + 2, columnspan=game.columns)
        
        visual.root.bind('<Return>', play_next_move)
        
        visual.manual_start()
