import random
from src.main.connect import ConnectXVisual, Agent, Matchup
import numpy as np
import pickle
from heuritic import heuritic

class BIGLEARNER:
    def __init__(self):
        self.learning_table = {}
        self.prev_board = None  # Initialized later
        self.prev_action = None  # Track previous action
        self.courage = 0.05  # Exploration rate
        self.alpha = 0.95 # Learning rate
        self.gamma = 0.95  # Discount factor

        self.random_moves = 0
        self.learned_moves = 0

    def load_learning_table(self):
        try:
            with open("./big_learner_learning_table", "rb") as learning_file:
                self.learning_table = pickle.load(learning_file)
        except FileNotFoundError:
            print("No learning table found")
        return

    def save_learing_table(self):
        with open("./big_learner_learning_table", "wb") as learning_file:
            pickle.dump(self.learning_table, learning_file)
        return

    def check_reward(self, board, win_length):
        unit_vectors = [
            [0, 1],
            [1, 0],
            [1, 1],
            [0, -1],
            [-1, 0],
            [-1, 1],
            [1, -1],
            [-1, -1],
        ]

        board_width = len(board)
        board_height = len(board[0])

        max_me, max_them = 0, 0
        for y in range(board_width):
            for x in range(board_height):
                for vector in unit_vectors:
                    count_me, count_them = 0, 0
                    for head in range(win_length):
                        head_x = x + head * vector[1]
                        head_y = y + head * vector[0]
                        if not (
                            0 <= head_x < board_height and 0 <= head_y < board_width
                        ):
                            break
                        pos = board[head_y][head_x]
                        if pos is None:
                            break
                        if pos == self.new_agent_who_dis():
                            count_me += 1
                        else:
                            count_them += 1
                    max_me = max(max_me, count_me)
                    max_them = max(max_them, count_them)

        if max_me == win_length:
            return 10  # Win
        elif max_them == win_length:
            return -2  # Lost
        elif not any(None in col for col in board):
            return -1  # Tie
        elif max_me == win_length - 1:
            return 0.5  # Near win
        elif max_them == win_length - 1:
            return -0.5  # Near loss
        else:
            return 0

    def new_agent_who_dis(self):
        return "Big Learner"

    def take_turn(self, board, win_length, opponent_name):
        reward = self.check_reward(board, win_length)

        available_actions = [col for col in range(board.shape[0]) if None in board[col]]
        if not available_actions:
            return None  # No move possible

        board_tup = tuple(board.flatten())

        if board_tup not in self.learning_table:
            self.learning_table[board_tup] = np.zeros(7)

        # Choose action using exploration-exploitation tradeoff
        if random.random() < self.courage or board_tup not in self.learning_table:
            self.random_moves += 1
            action = random.choice(available_actions)
        else:
            self.learned_moves += 1
            q_values = self.learning_table[board_tup]
            filtered_q_values = {action: q_values[action] for action in available_actions}
            action = max(filtered_q_values, key=filtered_q_values.get)

        # Only update Q-table if it's not the first move
        if self.prev_board is not None and self.prev_action is not None:
            prev_board_tup = tuple(self.prev_board.flatten())

            if prev_board_tup not in self.learning_table:
                self.learning_table[prev_board_tup] = np.zeros(7)

            # Bellman equation update
            self.learning_table[prev_board_tup][
                self.prev_action
            ] += self.alpha * (
                reward + self.gamma * np.max(self.learning_table[board_tup])
                - self.learning_table[prev_board_tup][self.prev_action]
            )

        # Store the new state for next round
        self.prev_action = action
        self.prev_board = np.copy(board)

        # self.courage = max(self.courage * 0.9,self.min_courage)
        return action


# Random agent that picks a random column
def get_random_agent_1_name():
    return "Random Agent 1"


def random_agent_1(board, win_length, opponent_name):
    available_actions = [col for col in range(board.shape[0]) if None in board[col]]
    if len(available_actions) > 0:
        return random.choice(available_actions)
    else:
        return

big_learner = BIGLEARNER()
big_learner.load_learning_table()
##### Visualizing the game ######
# # Playing a game manually
# visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_manual_game("X", "O")

# # Play a game against an agent
# visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_manual_against_agent("Human", "AI", agent_first_column, True, 1, 0.2)

# # Visualize a game between two agents
# visual = ConnectXVisual(7, 6, 4, 100, 100)
# visual.play_real_time_game("X", "O", agent_first_column, random_agent_1, 1, 2)

# Visualize X games between two agents (will alternate the starting player)
# visual = ConnectXVisual(7, 6, 4, 100, 100)
# agent_1: Agent = Agent("Big Learner", big_learner.take_turn)
# agent_2: Agent = Agent("heuritic", heuritic)
# visual.play_multiple_real_time_games(agent_1, agent_2, 1, 2, 1)

matchup: Matchup = Matchup(
    7,
    6,
    4,
    big_learner.new_agent_who_dis(),
    "heuritic",
    big_learner.take_turn,
    heuritic,
    1,
    5,
    100,
)
# Play a matchup
matchup.play_matchup()
print("hello")
big_learner.save_learing_table()
