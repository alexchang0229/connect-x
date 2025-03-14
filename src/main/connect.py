import numpy as np
import itertools
import tkinter as tk
from enum import Enum
from typing import Tuple, List, Callable
import threading
import copy
import os
import multiprocessing as mp


from typing import Callable, List, Dict





NO_WINNER_STATE: str = "NO_CLEAR_WINNER"
NO_WINNER_MESSAGE: str = "NO CLEAR WINNER. The difference in win percentage is less than the threshold."





class GameState(str, Enum):
    """
    Enum representing the possible states of a Connect X game.
    """
    DRAW = "DRAW"
    WIN = "WIN"
    IN_PROGRESS = "IN_PROGRESS"
    ILLEGAL_MOVE = "ILLEGAL_MOVE"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    AGENT_ERROR = "AGENT_ERROR"






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

    def register_agent_error(self, player: str, error_message: str) -> None:
        """
        Register an error that occurred during an agent's move.
        The player who made the error automatically loses the game.
        
        Args:
            player (str): The player who made the error.
            error_message (str): The error message.
            
        Returns:
            None
        """
        # Update game state
        self.game_state = GameState.AGENT_ERROR
        self.winner = self.get_other_player(player)
        self.previous_player_who_played = player
        
        # Add log messages
        message = f"Player {player} caused an error and lost: {error_message}"
        self.log.append(message)
        print(message)

    def check_illegal_move(self, column: int, player: str) -> Tuple[GameState, str]:
        # Check if player exists
        if player not in [self.FIRST_PLAYER_NAME, self.SECOND_PLAYER_NAME]:
            raise Exception(f"Error, player {player} is not in the game.")
        # Check if the game is in progress.
        if self.game_state != GameState.IN_PROGRESS:
            raise Exception(f"Error, tried to play while in terminal state. Cannot play in game state: {self.game_state}")
        # Check if column is an integer.
        try:
            int(column)
        except:
            return GameState.ILLEGAL_MOVE, "Column must be an integer."
        # Check if the column is valid.
        if column < 0 or column >= self.COLUMNS:
            return GameState.ILLEGAL_MOVE, "Played outside of the board."
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
            self.winner = self.get_other_player(player)
            self.previous_player_who_played = player
            self.log.append(message)
            self.log.append(f"Player {player} tried to play in full column {column} and lost.")
            print(message)
            return False
        # Make sure to convert the column to an integer
        # At this point, we know the column is valid, but it may be a string, or another castable type.
        column = int(column)
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

    def __eq__(self, other):
        if not isinstance(other, ConnectXMatch):
            return False
        return (
            self.COLUMNS == other.COLUMNS and
            self.ROWS == other.ROWS and
            self.WIN_LENGTH == other.WIN_LENGTH and
            self.FIRST_PLAYER_NAME == other.FIRST_PLAYER_NAME and
            self.SECOND_PLAYER_NAME == other.SECOND_PLAYER_NAME and
            np.array_equal(self.board, other.board) and
            self.game_state == other.game_state and
            self.winner == other.winner and
            self.previous_player_who_played == other.previous_player_who_played
            # self.moves_played == other.moves_played and
            # self.log == other.log
        )

    def copy(self):
        return copy.deepcopy(self)
    
    def deepcopy(self):
        new_instance = ConnectXMatch(
            self.COLUMNS,
            self.ROWS,
            self.WIN_LENGTH,
            self.FIRST_PLAYER_NAME,
            self.SECOND_PLAYER_NAME
        )
        new_instance.board = copy.deepcopy(self.board)
        new_instance.game_state = self.game_state
        new_instance.winner = self.winner
        new_instance.previous_player_who_played = self.previous_player_who_played
        new_instance.moves_played = copy.deepcopy(self.moves_played)
        new_instance.log = copy.deepcopy(self.log)
        return new_instance
    
    def __deepcopy__(self, memo):
        return self.deepcopy()

    def getPossibleActions(self) -> List[int]:
        legal_actions = []
        for column in range(self.COLUMNS):
            if not all(self.board[column] != None):
                legal_actions.append(column)
        return legal_actions
    
    def takeAction(self, action: int):
        new_match: ConnectXMatch = self.deepcopy()
        if self.previous_player_who_played is None:
            new_match.make_move(action, self.FIRST_PLAYER_NAME)
        new_match.make_move(action, self.get_other_player(self.previous_player_who_played))
        return new_match
    
    def isTerminal(self) -> bool:
        return self.game_state != GameState.IN_PROGRESS
    
    def getReward(self) -> int:
        if self.game_state == GameState.WIN:
            return 1 if self.winner == self.FIRST_PLAYER_NAME else -1
        elif self.game_state == GameState.DRAW:
            return 0
        else:
            raise Exception("Game is not in terminal state. Cannot get reward.")






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
        time_limit: int,
        enable_thread_protection: bool = True
    ):
        self.game: ConnectXMatch = ConnectXMatch(columns, rows, win_length, first_player_name, second_player_name)
        self.first_player_name = first_player_name
        self.second_player_name = second_player_name
        self.first_player_func: Callable = first_player_func
        self.second_player_func: Callable = second_player_func
        self.time_limit: float = time_limit
        self.enable_thread_protection: bool = enable_thread_protection

    def play_move_with_agent(self, player: str) -> bool:
        """
        This method plays a move with the agent specified by the player argument.
        This method creates a new thread to enforce the time limit when enable_thread_protection is True.
        Otherwise, it calls the agent function directly.

        Args:
            player (str): The player who is making the move.

        Returns:
            bool: True if the game goes on, False otherwise.
        """
        # Get the appropriate function for the player
        func: Callable = self.first_player_func if player == self.game.FIRST_PLAYER_NAME else self.second_player_func
        
        if self.enable_thread_protection:
            # Create a nested function to run the agent function
            column_answer = None
            agent_error = None
            
            def agent_move():
                nonlocal column_answer, agent_error
                try:
                    board_copy: np.ndarray = copy.deepcopy(self.game.board)
                    opponent_name = self.game.get_other_player(player)
                    column_answer = func(board_copy, self.game.WIN_LENGTH, opponent_name)
                except Exception as e:
                    agent_error = str(e)

            # Call the function in a thread
            move_thread = threading.Thread(target=agent_move)
            move_thread.start()
            # Start the thread and wait until the function returns or the time limit is exceeded.
            move_thread.join(timeout=self.time_limit)
            
            # Handle agent error if it occurred
            if agent_error is not None:
                self.game.register_agent_error(player, agent_error)
                return False
                
            # UPDATE STATE FOR TIME LIMIT EXCEEDED
            if move_thread.is_alive():
                self.game.game_state = GameState.TIME_LIMIT_EXCEEDED
                self.game.winner = self.game.get_other_player(player)
                self.previous_player_who_played = player
                message = f"Player {player} exceeded the time limit and lost."
                self.game.log.append(message)
                print(message)
                return GameState.TIME_LIMIT_EXCEEDED
            # If the thread finished on time, make the move
            return self.game.make_move(column_answer, player)
        else:
            # Call the agent function directly without thread protection
            try:
                board_copy: np.ndarray = copy.deepcopy(self.game.board)
                opponent_name = self.game.get_other_player(player)
                column_answer = func(board_copy, self.game.WIN_LENGTH, opponent_name)
                return self.game.make_move(column_answer, player)
            except Exception as e:
                self.game.register_agent_error(player, str(e))
                return False

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
        
        # After the game is over, inform both agents about the final state
        try:
            # Call first agent with final state
            board_copy: np.ndarray = copy.deepcopy(self.game.board)
            self.first_player_func(board_copy, self.game.WIN_LENGTH, self.second_player_name)
        except Exception as e:
            # Ignore any errors that might occur
            print(f"Error when informing {self.first_player_name} about final state: {e}")
            
        try:
            # Call second agent with final state
            board_copy: np.ndarray = copy.deepcopy(self.game.board)
            self.second_player_func(board_copy, self.game.WIN_LENGTH, self.first_player_name)
        except Exception as e:
            # Ignore any errors that might occur
            print(f"Error when informing {self.second_player_name} about final state: {e}")
            
        return self.game.winner








class BoardDimension:
    def __init__(
        self,
        columns: int,
        rows: int,
    ):
        self.columns: int = columns
        self.rows: int = rows

class Agent:
    def __init__(
        self,
        name: str,
        func: Callable
    ):
        self.name: str = name
        self.func: Callable = func


class Matchup:
    def __init__(
        self,
        board_dimension: BoardDimension,
        win_length: int,
        first_agent: Agent,
        second_agent: Agent,
        time_limit: int,
        win_percentage_threshold_for_win: float,
        enable_thread_protection: bool = True
    ):
        self.board_dimension: BoardDimension = board_dimension
        self.win_length: int = win_length
        self.first_agent: Agent = first_agent
        self.second_agent: Agent = second_agent
        self.win_percentage_threshold_for_win: float = win_percentage_threshold_for_win
        self.time_limit: float = time_limit
        self.enable_thread_protection: bool = enable_thread_protection

        self.first_player_wins: int = 0
        self.second_player_wins: int = 0
        self.draws: int = 0

        self.saved_player_1_games: List[ConnectXMatch] = []
        self.saved_player_2_games: List[ConnectXMatch] = []

        self.percentage_first_player_wins: float = None
        self.percentage_second_player_wins: float = None
        self.percentage_draws: float = None
        self.winner: str = None

    def play_n_games(self, number_of_games: int):
        current_agent: Agent = self.first_agent
        opponent_agent: Agent = self.second_agent
        
        for i in range(number_of_games):
            print(f"Playing game: {i}")
            game = ConnectXMatchWithAgents(
                self.board_dimension.columns,
                self.board_dimension.rows,
                self.win_length,
                current_agent.name,
                opponent_agent.name,
                current_agent.func,
                opponent_agent.func,
                self.time_limit,
                self.enable_thread_protection
            )
            winner = game.play_full_game()
            if winner == self.first_agent.name:
                self.first_player_wins += 1
                if len(self.saved_player_1_games) < 5:
                    self.saved_player_1_games.append(game.game)
            elif winner == self.second_agent.name:
                self.second_player_wins += 1
                if len(self.saved_player_2_games) < 5:
                    self.saved_player_2_games.append(game.game)
            else:
                self.draws += 1
            
            # Update analytics after each game
            self.update_analytics()
            
            # Switch players
            current_agent, opponent_agent = opponent_agent, current_agent
            
    @staticmethod
    def _play_single_game(game_index: int, board_dimension: BoardDimension, win_length: int, 
                         first_agent: Agent, second_agent: Agent, time_limit: float, 
                         enable_thread_protection: bool, start_with_first_agent: bool) -> Tuple[str, ConnectXMatch]:
        """
        Worker function to play a single game for parallelism.
        
        Returns:
            Tuple[str, ConnectXMatch]: The winner of the game and the game object
        """
        print(f"Playing game: {game_index}")
        
        if start_with_first_agent:
            current_agent = first_agent
            opponent_agent = second_agent
        else:
            current_agent = second_agent
            opponent_agent = first_agent
            
        game = ConnectXMatchWithAgents(
            board_dimension.columns,
            board_dimension.rows,
            win_length,
            current_agent.name,
            opponent_agent.name,
            current_agent.func,
            opponent_agent.func,
            time_limit,
            enable_thread_protection
        )
        
        winner = game.play_full_game()
        return (winner, game.game)
            
    def play_n_games_with_parallelism(self, number_of_games: int, num_processes: int = None):
        """
        Play multiple games in parallel using multiprocessing.
        
        Args:
            number_of_games (int): Number of games to play
            num_processes (int, optional): Number of processes to use. Defaults to CPU count.
        """ 
        if num_processes is None:
            num_processes = mp.cpu_count()
        
        # Prepare arguments for each game, alternating which player starts
        game_args = []
        for i in range(number_of_games):
            start_with_first_agent = (i % 2 == 0)  # Alternate starting player
            game_args.append((
                i,  # game_index
                self.board_dimension,  # board_dimension
                self.win_length,  # win_length
                self.first_agent,  # first_agent
                self.second_agent,  # second_agent
                self.time_limit,  # time_limit
                self.enable_thread_protection,  # enable_thread_protection
                start_with_first_agent  # start_with_first_agent
            ))
        
        # Play games in parallel
        with mp.Pool(processes=num_processes) as pool:
            results = pool.starmap(Matchup._play_single_game, game_args)
        
        # Process results
        for winner, game in results:
            if winner == self.first_agent.name:
                self.first_player_wins += 1
                if len(self.saved_player_1_games) < 5:
                    self.saved_player_1_games.append(game)
            elif winner == self.second_agent.name:
                self.second_player_wins += 1
                if len(self.saved_player_2_games) < 5:
                    self.saved_player_2_games.append(game)
            else:
                self.draws += 1
        
        # Update analytics after all games
        self.update_analytics()

    def update_analytics(self):
        total_games = self.first_player_wins + self.second_player_wins + self.draws
        if total_games == 0:
            self.percentage_first_player_wins = 0.0
            self.percentage_second_player_wins = 0.0
            self.percentage_draws = 0.0
            self.winner = NO_WINNER_MESSAGE
            return self.winner
            
        self.percentage_first_player_wins = (self.first_player_wins / total_games) * 100
        self.percentage_second_player_wins = (self.second_player_wins / total_games) * 100
        self.percentage_draws = (self.draws / total_games) * 100
        # Decide the winner, if winner there is.
        self.winner = self.determine_winner()
        return self.winner

    def determine_winner(self) -> str:
        if self.percentage_first_player_wins >= self.percentage_second_player_wins + self.win_percentage_threshold_for_win:
            return self.first_agent.name
        elif self.percentage_second_player_wins >= self.percentage_first_player_wins + self.win_percentage_threshold_for_win:
            return self.second_agent.name
        else:
            return NO_WINNER_MESSAGE
        
    def get_report_lines(self) -> List[str]:
        total_games = self.first_player_wins + self.second_player_wins + self.draws
        return [
            "Connect X Matchup Report",
            "========================",
            f"Columns: {self.board_dimension.columns}",
            f"Rows: {self.board_dimension.rows}",
            f"Win Length: {self.win_length}",
            f"First Player: {self.first_agent.name}",
            f"Second Player: {self.second_agent.name}",
            f"Total Games Played: {total_games}",
            f"Time Limit: {self.time_limit} seconds",
            f"Win Percentage Threshold for Win: {self.win_percentage_threshold_for_win}",
            "",
            "Results:",
            f"First Player Wins: {self.first_player_wins} ({self.percentage_first_player_wins})",
            f"Second Player Wins: {self.second_player_wins} ({self.percentage_second_player_wins})",
            f"Draws: {self.draws} ({self.percentage_draws})",
            "",
            f"Winner: {self.winner}",
            "========================"
        ]
        
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

        with open(file_path, 'w') as file:
            file.write("\n".join(self.get_report_lines()))






class MetaMatchup:
    def __init__(
        self,
        board_dimensions: List[BoardDimension],
        win_lengths: List[int],
        first_agent: Agent,
        second_agent: Agent,
        turn_time_limit_s: int,
        win_percentage_threshold_for_win: float,
        number_of_games_per_matchup: int,
        enable_thread_protection: bool = True
    ):
        # Parameters
        self.board_dimensions: List[BoardDimension] = board_dimensions
        self.win_lengths: List[int] = win_lengths
        self.first_agent: Agent = first_agent
        self.second_agent: Agent = second_agent
        self.turn_time_limit_s: int = turn_time_limit_s
        self.win_percentage_threshold_for_win: float = win_percentage_threshold_for_win
        self.number_of_games_per_matchup: int = number_of_games_per_matchup
        self.enable_thread_protection: bool = enable_thread_protection

        # Matchups
        self.matchups: List[Matchup] = []
        
        # Analysis
        self.overall_total_games: int = 0
        self.overall_first_player_wins: int = 0
        self.overall_second_player_wins: int = 0
        self.overall_draws: int = 0
        self.overall_percentage_first_player_wins: float = None
        self.overall_percentage_second_player_wins: float = None
        self.overall_percentage_draws: float = None
        self.overall_winner: str = None
    
    def play_matchups(self):
        for board_dimension in self.board_dimensions:
            for win_length in self.win_lengths:
                matchup = Matchup(
                    board_dimension,
                    win_length,
                    self.first_agent,
                    self.second_agent,
                    self.turn_time_limit_s,
                    self.win_percentage_threshold_for_win,
                    self.enable_thread_protection
                )
                matchup.play_n_games(self.number_of_games_per_matchup)
                self.matchups.append(matchup)
        self.analyse_matchups()

    def play_matchup_in_process(matchup_data: Tuple[BoardDimension, int, Agent, Agent, int, float, int, bool], results_list: List[Matchup]):
        """Worker function to run play_matchup() and store results."""
        board_dimension, win_length, first_agent, second_agent, time_limit, win_percentage_threshold, num_games, enable_thread_protection = matchup_data
        matchup = Matchup(board_dimension, win_length, first_agent, second_agent, time_limit, win_percentage_threshold, enable_thread_protection)
        matchup.play_n_games(num_games)
        results_list.append(matchup)

    def play_parallel_matchups(self):
        with mp.Manager() as manager:
            shared_results: List[Matchup] = manager.list()
            matchups_data = []
            for board_dimension in self.board_dimensions:
                for win_length in self.win_lengths:
                    print(f"Playing matchup between {self.first_agent.name} and {self.second_agent.name}")
                    matchup_data: Tuple[BoardDimension, int, Agent, Agent, int, float, int, bool] = (
                        board_dimension,
                        win_length,
                        self.first_agent,
                        self.second_agent,
                        self.turn_time_limit_s,
                        self.win_percentage_threshold_for_win,
                        self.number_of_games_per_matchup,
                        self.enable_thread_protection
                    )
                    matchups_data.append(matchup_data)
            with mp.Pool(mp.cpu_count()) as pool:
                pool.starmap(MetaMatchup.play_matchup_in_process, [(matchup_data, shared_results) for matchup_data in matchups_data])
            self.matchups = list(shared_results)
        self.analyse_matchups()

    def analyse_matchups(self):
        self.overall_total_games = sum(matchup.first_player_wins + matchup.second_player_wins + matchup.draws for matchup in self.matchups)
        self.overall_first_player_wins = sum(matchup.first_player_wins for matchup in self.matchups)
        self.overall_second_player_wins = sum(matchup.second_player_wins for matchup in self.matchups)
        self.overall_draws = sum(matchup.draws for matchup in self.matchups)
        self.overall_percentage_first_player_wins = (self.overall_first_player_wins / self.overall_total_games) * 100
        self.overall_percentage_second_player_wins = (self.overall_second_player_wins / self.overall_total_games) * 100
        self.overall_percentage_draws = (self.overall_draws / self.overall_total_games) * 100
        # Decide the winner, if winner there is.
        self.overall_winner = self.determine_overall_winner()
        
    def determine_overall_winner(self) -> str:
        if self.overall_percentage_first_player_wins >= self.overall_percentage_second_player_wins + self.win_percentage_threshold_for_win:
            return self.first_agent.name
        elif self.overall_percentage_second_player_wins >= self.overall_percentage_first_player_wins + self.win_percentage_threshold_for_win:
            return self.second_agent.name
        else:
            return NO_WINNER_MESSAGE

    def generate_report(self, file_path: str):
        """
        Generate a report of the matchup and print it to a specified text file.

        Args:
            file_path (str): The path of the file to print the report to.

        Raises:
            Exception: If the matchup has not occurred yet.
        """
        if not hasattr(self, 'overall_winner'):
            raise Exception("The meta matchup has not occurred yet. Please run the meta matchup before generating a report.")
        
        matchups_report_lines: List[str] = []
        for matchup in self.matchups:
            matchups_report_lines += matchup.get_report_lines()
            matchups_report_lines.append("")

        report_lines = [
            "Connect X Meta Matchup Report",
            "========================",
            "Agents:",
            f"First Agent: {self.first_agent.name}",
            f"Second Agent: {self.second_agent.name}",
            "",
            "Results:",
            f"Total Games: {self.overall_total_games}",
            f"{self.first_agent.name}: {self.overall_first_player_wins} ({self.overall_percentage_first_player_wins})",
            f"{self.second_agent.name}: {self.overall_second_player_wins} ({self.overall_percentage_second_player_wins})",
            f"Draws: {self.overall_draws} ({self.overall_percentage_draws})",
            "",
            f"Winner: {self.overall_winner}",
            "========================",
            "",
            "",
            "",
            "",
            "",
            "Matchups:",
            ""
        ]
        report_lines += matchups_report_lines
        with open(file_path, 'w') as file:
            file.write("\n".join(report_lines))






class Tournament:
    def __init__(
        self,
        board_dimensions: List[BoardDimension],
        win_lengths: List[int],
        agents: List[Agent],
        turn_time_limit_s: int,
        win_percentage_threshold_for_win: float,
        number_of_games_per_matchup: int
    ):
        # Parameters
        self.board_dimensions: List[BoardDimension] = board_dimensions
        self.win_lengths: List[int] = win_lengths
        self.agents: List[Agent] = agents
        self.turn_time_limit_s: int = turn_time_limit_s
        self.win_percentage_threshold_for_win: float = win_percentage_threshold_for_win
        self.number_of_games_per_matchup: int = number_of_games_per_matchup

        # Meta Matchups
        self.meta_matchups: List[MetaMatchup] = []

        # Analysis
        self.agents_metamatchup_wins: Dict[str, int] = {}
        for agent in self.agents:
            self.agents_metamatchup_wins[agent.name] = 0
        self.agents_metamatchup_wins[NO_WINNER_STATE] = 0
        self.overall_winner: str = None

    def play_tournament(self, file_dir: str = None, enable_thread_protection: bool = True):
        for agent_1, agent_2 in itertools.combinations(self.agents, 2):
            print(f"Playing meta matchup between {agent_1.name} and {agent_2.name}")
            meta_matchup = MetaMatchup(
                self.board_dimensions,
                self.win_lengths,
                agent_1,
                agent_2,
                self.turn_time_limit_s,
                self.win_percentage_threshold_for_win,
                self.number_of_games_per_matchup,
                enable_thread_protection
            )
            meta_matchup.play_matchups()
            if file_dir is not None:
                # If the directory does not exist, create it.
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                meta_matchup.generate_report(file_path=file_dir + f"/{agent_1.name}_vs_{agent_2.name}.txt")
            self.meta_matchups.append(meta_matchup)
        self.analyse_tournament()

    def analyse_tournament(self):
        for meta_matchup in self.meta_matchups:
            if meta_matchup.overall_winner is not None:
                if meta_matchup.overall_winner == NO_WINNER_MESSAGE:
                    self.agents_metamatchup_wins[NO_WINNER_STATE] += 1
                else:    
                    self.agents_metamatchup_wins[meta_matchup.overall_winner] += 1
                
        self.overall_winner = self.determine_overall_winner()

    def determine_overall_winner(self) -> str:
        # No clear winner if two agents have the same number of wins
        max_wins = max(self.agents_metamatchup_wins.values())
        if list(self.agents_metamatchup_wins.values()).count(max_wins) > 1:
            return NO_WINNER_STATE
        return max(self.agents_metamatchup_wins, key=self.agents_metamatchup_wins.get)
    
    def generate_reports_in_dir(self, file_dir: str):
        """
        Generate a report of the matchup and print it to a specified text file.

        Args:
            file_dir (str): The path of the file to print the report to.

        Raises:
            Exception: If the matchup has not occurred yet.
        """
        # If the directory does not exist, create it.
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if not hasattr(self, 'overall_winner'):
            raise Exception("The tournament has not occurred yet. Please run the tournament before generating a report.")
        report_lines = [
            "Connect X Tournament Report",
            "========================",
            "Agents:",
            "\n".join([f"{agent.name}: {self.agents_metamatchup_wins[agent.name]}" for agent in self.agents]),
            "",
            "Results:",
            f"Winner: {self.overall_winner}",
            "========================",
        ]
        with open(file_dir + "/tournament_result.txt", 'w') as file:
            file.write("\n".join(report_lines) + "\n")

        # Generate meta matchup reports
        for meta_matchup in self.meta_matchups:
            meta_matchup.generate_report(file_path=file_dir + f"/{meta_matchup.first_agent.name}_vs_{meta_matchup.second_agent.name}.txt")






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
        self.paused = False

    def update_board(self, match: ConnectXMatch):
        for col in range(match.COLUMNS):
            for row in range(match.ROWS):
                value = match.board[col][row]
                color = "white" if value is None else ("red" if value == match.FIRST_PLAYER_NAME else "yellow")
                x = col
                y = match.ROWS - row - 1  # Invert the row index
                canvas = self.cells[x][y]
                canvas.delete("all")
                if value is not None:
                    canvas.create_oval(5, 5, self.width-5, self.height-5, fill=color)
                    canvas.create_text(self.width/2, self.height/2, text=value, fill="black")

        if match.game_state == GameState.WIN:
            winner_color = "green"
            self.result_label.config(text=f"{match.winner} wins!", font=("Helvetica", 24), fg=winner_color)
            self.state_label.config(text="Game over")
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
            self.result_label.config(text=f"{match.winner} wins! {match.get_other_player(match.winner)} lost due to {'illegal move' if match.game_state == GameState.ILLEGAL_MOVE else 'time limit exceeded'}.", font=("Helvetica", 24), fg="red")
            self.state_label.config(text="Game over")
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)
        elif match.game_state == GameState.DRAW:
            for col in range(match.COLUMNS):
                for row in range(match.ROWS):
                    self.cells[col][row].config(bg="yellow")
            self.result_label.config(text="The game is a draw. No winners.", font=("Helvetica", 24), fg="yellow")
            self.state_label.config(text="Game over")
            self.game_over = True
            for button in self.buttons:
                button.config(state=tk.DISABLED)
        else:
            current_player = match.get_other_player(match.previous_player_who_played) if match.previous_player_who_played else match.FIRST_PLAYER_NAME
            self.state_label.config(text=f"Turn: {current_player}")

    def setup(self, button_method: Callable):
        self.root = tk.Tk()
        self.root.title("Connect X")

        self.state_label = tk.Label(self.root, text="Turn: Player 1", font=("Helvetica", 16))
        self.state_label.grid(row=0, columnspan=self.columns)

        self.cells = [[tk.Canvas(self.root, width=100, height=100, bg="white", borderwidth=2, relief="groove") for _ in range(self.rows)] for _ in range(self.columns)]
        for col in range(self.columns):
            for row in range(self.rows):
                self.cells[col][row].grid(row=row+1, column=col)

        self.buttons = [tk.Button(self.root, text=f"Drop {col+1}", command=lambda col=col: button_method(col)) for col in range(self.columns)]
        for col, button in enumerate(self.buttons):
            button.grid(row=self.rows+1, column=col)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=self.rows+2, columnspan=self.columns)

        self.root.bind("<Return>", self.toggle_pause)
        self.root.bind("<space>", self.toggle_pause)

    def toggle_pause(self, event):
        self.paused = not self.paused
        if self.paused:
            self.state_label.config(text="Game paused")
        else:
            self.state_label.config(text="Game resumed")
            self.play_next_move()

    def manual_start(self):
        self.root.mainloop()

    def play_manual_game(self, agent_1_name: str, agent_2_name: str):
        """
        Play a manual game between two agents.

        Args:
            agent_1_name (str): Name of the first agent.
            agent_2_name (str): Name of the second agent.
        """
        game = ConnectXMatch(self.columns, self.rows, self.win_length, agent_1_name, agent_2_name)

        def play_next_move(column):
            if self.game_over:
                return
            game.play_with_next_player(column)
            self.update_board(game)
            if game.game_state in [GameState.WIN, GameState.ILLEGAL_MOVE, GameState.TIME_LIMIT_EXCEEDED, GameState.DRAW]:
                self.game_over = True

        self.setup(play_next_move)
        self.manual_start()

    def play_real_time_game(self, agent_1_name: str, agent_2_name: str, agent_1_func: Callable, agent_2_func: Callable, agents_turn_time_limit_seconds: int, time_between_moves_for_visualization_seconds: int):
        """
        Play a real-time game between two agents.

        Args:
            agent_1_name (str): Name of the first agent.
            agent_1_func (Callable): Function for the first agent.
            agent_2_name (str): Name of the second agent.
            agent_2_func (Callable): Function for the second agent.
            time_limit (int): Time limit for each move in seconds.
        """
        self.game_with_agents = ConnectXMatchWithAgents(
            self.columns,
            self.rows,
            self.win_length,
            agent_1_name,
            agent_2_name,
            agent_1_func,
            agent_2_func,
            agents_turn_time_limit_seconds
        )

        def play_next_move():
            if not self.paused and self.game_with_agents.game.game_state == GameState.IN_PROGRESS:
                self.game_with_agents.play_move_with_next_agent()
                self.update_board(self.game_with_agents.game)
                if self.game_with_agents.game.game_state == GameState.IN_PROGRESS:
                    time_between_moves_for_visualization_milliseconds = time_between_moves_for_visualization_seconds * 1000
                    self.root.after(time_between_moves_for_visualization_milliseconds, play_next_move)

        self.play_next_move = play_next_move
        self.setup(play_next_move)
        play_next_move()
        self.root.mainloop()

    def play_manual_against_agent(
        self, 
        human_name: str, 
        agent_name: str, 
        agent_func: Callable, 
        human_starts: bool, 
        agents_turn_time_limit_seconds: int, 
        time_between_moves_for_visualization_seconds: int = 0.2
    ):
        """
        Play a game between a human and an agent.

        Args:
            human_name (str): Name of the human player.
            agent_name (str): Name of the agent.
            agent_func (Callable): Function for the agent.
            human_starts (bool): If True, the human starts. Otherwise, the agent starts.
            agents_turn_time_limit_seconds (int): Time limit for the agent's move in seconds.
            time_between_moves_for_visualization_seconds (int): Time between moves for visualization in seconds.
        """
        game_with_agents = ConnectXMatchWithAgents(
            self.columns,
            self.rows,
            self.win_length,
            human_name if human_starts else agent_name,
            agent_name if human_starts else human_name,
            None if human_starts else agent_func,
            agent_func if human_starts else None,
            agents_turn_time_limit_seconds
        )

        def play_next_move(column=None):
            if game_with_agents.game.game_state == GameState.IN_PROGRESS:
                if game_with_agents.game.previous_player_who_played == human_name:
                    game_with_agents.play_move_with_agent(agent_name)
                else:
                    game_with_agents.game.play_with_next_player(column)
                self.update_board(game_with_agents.game)
                if game_with_agents.game.game_state == GameState.IN_PROGRESS and game_with_agents.game.previous_player_who_played == human_name:
                    time_between_moves_for_visualization_milliseconds = int(time_between_moves_for_visualization_seconds * 1000)
                    self.root.after(time_between_moves_for_visualization_milliseconds, play_next_move)

        self.setup(play_next_move)
        if not human_starts:
            play_next_move()
        self.root.mainloop()

    def play_multiple_real_time_games(
        self, 
        first_agent: Agent,
        second_agent: Agent,
        agents_turn_time_limit_s: int,
        time_between_moves_for_visualization_s: int,
        number_of_games: int,
    ):
        
        for _ in range(int(number_of_games/2)):
            visual = ConnectXVisual(7, 6, 4)
            visual.play_real_time_game(
                first_agent.name, 
                second_agent.name, 
                first_agent.func, 
                second_agent.func, 
                agents_turn_time_limit_s, 
                time_between_moves_for_visualization_s
            )
            visual = ConnectXVisual(7, 6, 4)
            visual.play_real_time_game(
                second_agent.name,
                first_agent.name,
                second_agent.func,
                first_agent.func,
                agents_turn_time_limit_s,
                time_between_moves_for_visualization_s
            )
        if number_of_games % 2 == 1:
            visual = ConnectXVisual(7, 6, 4)
            visual.play_real_time_game(
                first_agent.name, 
                second_agent.name, 
                first_agent.func, 
                second_agent.func, 
                agents_turn_time_limit_s, 
                time_between_moves_for_visualization_s
            )