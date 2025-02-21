from src.main.connect import Matchup, ConnectXVisual, Agent, BoardDimension, MetaMatchup, Tournament
import random




##### THRESHOLD AGENTS #####
from competition.week_2.agents.threshold_week_2 import heuritic, columnator

threshold_columnator: Agent = Agent("columnator", columnator)
threshold_heuritic: Agent = Agent("heuritic", heuritic)




##### WEEK AGENTS #####
def random_move(board, win_length, opponent_name):
    return random.randint(0, board.shape[0] - 1)

# from competition.week_2.agents import 
nathaniel: Agent = Agent("placeholder_1", random_move)
alex = Agent("placeholder_2", random_move)
sam = Agent("placeholder_3", random_move)



##### TOURNAMENT #####
def play_tournament():
    agents = [threshold_columnator, threshold_heuritic, nathaniel, alex, sam]
    board_dimensions = [
        BoardDimension(7, 6), 
        BoardDimension(8, 7),
        BoardDimension(9, 8),
        BoardDimension(10, 10)]
    win_lengths = [4, 5, 6]
    tournament: Tournament = Tournament(
        board_dimensions,
        win_lengths,
        agents,
        turn_time_limit_s=1,
        win_percentage_threshold_for_win=5,
        number_of_games_per_matchup=100
    )
    tournament.play_tournament()
    tournament.generate_reports_in_dir("competition/week_2/results")



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

# # Visualize X games between two agents (will alternate the starting player)
# visual = ConnectXVisual(7, 6, 4, 100, 100)
# agent_1: Agent = Agent("Agent1", agent_first_column)
# agent_2: Agent = Agent("Agent2", random_agent_1)
# visual.play_multiple_real_time_games(agent_1, agent_2, 1, 2, 3)


if __name__ == "__main__":
    play_tournament()

