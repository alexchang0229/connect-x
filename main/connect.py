import numpy as np
import itertools
import tkinter as tk
from enum import Enum
from typing import Tuple, List, Callable
import threading

from typing import Callable






class GameState(str, Enum):
    """
    Enum representing the possible states of a Connect X game.
    """
    DRAW = "DRAW"
    WIN = "WIN"
    IN_PROGRESS = "IN_PROGRESS"
    ILLEGAL_MOVE = "ILLEGAL_MOVE"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"






class ConnectXMatch:
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
                break
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






class ConnectXMatchWithAgents:
    def __init__(
        self,
        columns: int,
        rows: int,
        win_length: int,
        first_player_name: str,
        second_player_name: str,
        first_player_func: Callable,
        second_player_func: Callable,
        time_limit: int
    ):
        self.game: ConnectXMatch = ConnectXMatch(columns, rows, win_length, first_player_name, second_player_name)
        self.first_player_func: Callable = first_player_func
        self.second_player_func: Callable = second_player_func
        self.time_limit: float = time_limit

    def play_move_with_agent(self, player: str) -> bool:
        """
        This method plays a move with the agent specified by the player argument.
        This method creates a new thread to enforce the time limit.

        Args:
            player (str): The player who is making the move.

        Returns:
            bool: True if the game goes on, False otherwise.
        """
        # Create a nested function to run the agent function
        column_answer = None
        def agent_move():
            nonlocal column_answer
            column_answer = func(self.game.board, self.game.WIN_LENGTH)

        # Call the function in a thread
        func: Callable = self.first_player_func if player == self.game.FIRST_PLAYER_NAME else self.second_player_func
        move_thread = threading.Thread(target=agent_move)
        move_thread.start()
        # Start the thread and wait until the function returns or the time limit is exceeded.
        move_thread.join(timeout=self.time_limit)
        # UPDATE STATE FOR TIME LIMIT EXCEEDED
        if move_thread.is_alive():
            self.game.game_state = GameState.TIME_LIMIT_EXCEEDED
            self.game.winner = self.game.get_other_player(player)
            self.previous_player_who_played = player
            message = f"Player {player} exceeded the time limit and lost."
            self.game.log.append(message)
            print(message)
            return GameState.TIME_LIMIT_EXCEEDED
        else:
            # If the thread finished on time, make the move
            return self.game.make_move(column_answer, player)
        
    def play_move_with_next_agent(self) -> str:
        """
        This method plays a move with the agent specified by the player argument.
        This method creates a new thread to enforce the time limit.

        Args:
            player (str): The player who is making the move.

        Returns:
            bool: True if the game goes on, False otherwise.
        """
        # Determine the current player
        if self.game.previous_player_who_played is None:
            next_player: str = self.game.FIRST_PLAYER_NAME
        else:
            next_player: str = self.game.get_other_player(self.game.previous_player_who_played)
        return self.play_move_with_agent(next_player)

    def play_full_game(self) -> str:
        """
        This method plays a game between two agents.

        Returns:
            str: The name of the winning agent.
        """
        while self.game.game_state == GameState.IN_PROGRESS:
            self.play_move_with_next_agent()
        return self.game.winner






class ConnectXMatchup:
    def __init__(
        self,
        columns: int,
        rows: int,
        win_length: int,
        first_player_name: str,
        second_player_name: str,
        first_player_func: Callable,
        second_player_func: Callable,
        time_limit: int,
        win_percentage_threshold_for_win: float,
        number_of_games: int
    ):
        self.columns: int = columns
        self.rows: int = rows
        self.win_length: int = win_length
        self.first_player_name: str = first_player_name
        self.second_player_name: str = second_player_name
        self.first_player_func: Callable = first_player_func
        self.second_player_func: Callable = second_player_func
        self.win_percentage_threshold_for_win: float = win_percentage_threshold_for_win
        self.time_limit: float = time_limit
        self.number_of_games: int = number_of_games

        self.first_player_wins: int = 0
        self.second_player_wins: int = 0
        self.draws: int = 0

        self.saved_player_1_games: List[ConnectXMatch] = []
        self.saved_player_2_games: List[ConnectXMatch] = []

    def play_matchup(self) -> str:
        for _ in range(self.number_of_games):
            game = ConnectXMatchWithAgents(
                self.columns,
                self.rows,
                self.win_length,
                self.first_player_name,
                self.second_player_name,
                self.first_player_func,
                self.second_player_func,
                self.time_limit
            )
            winner = game.play_full_game()
            if winner == self.first_player_name:
                self.first_player_wins += 1
                if len(self.saved_player_1_games) < 5:
                    self.saved_player_1_games.append(game.game)
            elif winner == self.second_player_name:
                self.second_player_wins += 1
                if len(self.saved_player_2_games) < 5:
                    self.saved_player_2_games.append(game.game)
            else:
                self.draws += 1
        return self.analyse_matchup(self.first_player_wins, self.second_player_wins, self.draws)
    
    def analyse_matchup(self, first_player_wins, second_player_wins, draws):
        self.percentage_first_player_wins: float = first_player_wins / (first_player_wins + second_player_wins + draws)
        self.percentage_second_player_wins: float = second_player_wins / (first_player_wins + second_player_wins + draws)
        self.percentage_draws: float = draws / (first_player_wins + second_player_wins + draws)
        # Decide the winner, if winner there is.
        self.winner: str = self.determine_winner()
        return self.winner

    def determine_winner(self) -> str:
        if self.percentage_first_player_wins >= self.percentage_second_player_wins + self.win_percentage_threshold_for_win:
            return self.first_player_name
        elif self.percentage_second_player_wins >= self.percentage_first_player_wins + self.win_percentage_threshold_for_win:
            return self.second_player_name
        else:
            return "NO CLEAR WINNER. The difference in win percentage is less than the threshold."
        
    def generate_report(self, file_path: str):
        """
        Generate a report of the matchup and print it to a specified text file.

        Args:
            file_path (str): The path of the file to print the report to.

        Raises:
            Exception: If the matchup has not occurred yet.
        """
        if not hasattr(self, 'winner'):
            raise Exception("The matchup has not occurred yet. Please run the matchup before generating a report.")

        report_lines = [
            "Connect X Matchup Report",
            "========================",
            f"Columns: {self.columns}",
            f"Rows: {self.rows}",
            f"Win Length: {self.win_length}",
            f"First Player: {self.first_player_name}",
            f"Second Player: {self.second_player_name}",
            f"Number of Games: {self.number_of_games}",
            f"Time Limit: {self.time_limit} seconds",
            f"Win Percentage Threshold for Win: {self.win_percentage_threshold_for_win:.2%}",
            "",
            "Results:",
            f"First Player Wins: {self.first_player_wins} ({self.percentage_first_player_wins:.2%})",
            f"Second Player Wins: {self.second_player_wins} ({self.percentage_second_player_wins:.2%})",
            f"Draws: {self.draws} ({self.percentage_draws:.2%})",
            "",
            f"Winner: {self.winner}",
            "========================"
        ]

        with open(file_path, 'w') as file:
            file.write("\n".join(report_lines))



class ConnectXVisual:
    def __init__(
        self,
        columns: int,
        rows: int,
        win_length: int,
        width=100,
        height=100
    ):
        self.columns: int = columns
        self.rows: int = rows
        self.win_length: int = win_length
        self.width = width
        self.height = height
        self.game_over = False

    def update_board(self, match: ConnectXMatch):
        for col in range(match.COLUMNS):
            for row in range(match.ROWS):
                value = match.board[col][row]
                color = "white" if value is None else ("red" if value == self.agent_1_name else "yellow")
                x = col
                y = match.ROWS - row - 1  # Invert the row index
                canvas = self.cells[x][y]
                canvas.delete("all")
                if value is not None:
                    canvas.create_oval(5, 5, self.width-5, self.height-5, fill=color)
                    canvas.create_text(self.width/2, self.height/2, text=value, fill="black")

        if match.game_state == GameState.WIN:
            winner_color = "red" if self.player == self.agent_1_name else "yellow"
            self.result_label.config(text=f"{self.player} wins!", font=("Helvetica", 24), fg=winner_color)
            for col in range(match.COLUMNS):
                for row in range(match.ROWS):
                    self.cells[col][row].config(bg="light green")
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)
        elif match.game_state in [GameState.ILLEGAL_MOVE, GameState.TIME_LIMIT_EXCEEDED]:
            for col in range(match.COLUMNS):
                for row in range(match.ROWS):
                    self.cells[col][row].config(bg="red")
            self.result_label.config(text=f"{match.winner} wins! {self.player} lost due to {'illegal move' if match.game_state == GameState.ILLEGAL_MOVE else 'time limit exceeded'}.", font=("Helvetica", 24), fg="red")
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)
        elif match.game_state == GameState.DRAW:
            for col in range(match.COLUMNS):
                for row in range(match.ROWS):
                    self.cells[col][row].config(bg="yellow")
            self.result_label.config(text="The game is a draw. No winners.", font=("Helvetica", 24), fg="yellow")
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)

    def setup(self, button_method: Callable):
        self.root = tk.Tk()
        self.root.title("Connect X")

        self.cells = [[tk.Canvas(self.root, width=100, height=100, bg="white", borderwidth=2, relief="groove") for _ in range(self.rows)] for _ in range(self.columns)]
        for col in range(self.columns):
            for row in range(self.rows):
                self.cells[col][row].grid(row=row, column=col)

        self.buttons = [tk.Button(self.root, text=f"Drop {col+1}", command=lambda col=col: button_method(col)) for col in range(self.columns)]
        for col, button in enumerate(self.buttons):
            button.grid(row=self.rows, column=col)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=self.rows+1, columnspan=self.columns)

    def manual_start(self):
        self.root.mainloop()

    def automatic_timed_start(self, agent_1_func: Callable, agent_2_func: Callable, time_between_moves: int):
        def play_next_move():
            if self.game_over:
                return
            if self.player == self.agent_1_name:
                column = agent_1_func(self.game.board, self.game.WIN_LENGTH)
            else:
                column = agent_2_func(self.game.board, self.game.WIN_LENGTH)
            self.play_with_next_player(column)
            if not self.game_over:
                self.root.after(time_between_moves, play_next_move)

        self.setup(self.play_with_next_player)
        self.root.after(time_between_moves, play_next_move)
        self.root.mainloop()

    def play_real_time_game(self, agent_1_name: str, agent_1_func: Callable, agent_2_name: str, agent_2_func: Callable, time_limit: int):
        """
        Play a real-time game between two agents.

        Args:
            agent_1_name (str): Name of the first agent.
            agent_1_func (Callable): Function for the first agent.
            agent_2_name (str): Name of the second agent.
            agent_2_func (Callable): Function for the second agent.
            time_limit (int): Time limit for each move in seconds.
        """
        self.game = ConnectXMatchWithAgents(
            self.columns,
            self.rows,
            self.win_length,
            agent_1_name,
            agent_2_name,
            agent_1_func,
            agent_2_func,
            time_limit
        )

        def play_next_move():
            if self.game.game.game_state == GameState.IN_PROGRESS:
                self.game.play_move_with_next_agent()
                self.update_board(self.game.game)
                self.root.after(time_limit * 1000, play_next_move)

        self.setup(self.play_with_next_player)
        self.root.after(time_limit * 1000, play_next_move)
        self.root.mainloop()

    def play_manual_game(self, agent_1_name: str, agent_2_name: str):
        """
        Play a manual game between two agents.

        Args:
            agent_1_name (str): Name of the first agent.
            agent_2_name (str): Name of the second agent.
        """
        self.game = ConnectXMatch(self.columns, self.rows, self.win_length, agent_1_name, agent_2_name)
        self.agent_1_name = agent_1_name
        self.agent_2_name = agent_2_name
        self.player = agent_1_name

        def play_next_move(column):
            if self.game_over:
                return
            self.game.play_with_next_player(column)
            self.update_board(self.game)
            if self.game.game_state in [GameState.WIN, GameState.ILLEGAL_MOVE, GameState.TIME_LIMIT_EXCEEDED, GameState.DRAW]:
                self.game_over = True

        self.setup(play_next_move)
        self.manual_start()
