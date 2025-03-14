from competition.week_1.agents import columnator_and_heuritic, weak_1_ncc_play_winning_move
from src.main.connect import Matchup, BoardDimension, Agent

player_1_name = weak_1_ncc_play_winning_move.get_name()
player_1 = weak_1_ncc_play_winning_move.play
player_2_name = 'heuritic'
player_2 = columnator_and_heuritic.heuritic
player_3_name = 'columnator'
player_3 = columnator_and_heuritic.columnator

number_of_games = 100
board_dim = BoardDimension(7, 6)

# MATCHUP 1 and 2
agent_1 = Agent(player_1_name, player_1)
agent_2 = Agent(player_2_name, player_2)
matchup_1_2: Matchup = Matchup(board_dim, 4, agent_1, agent_2, 2, 1)
matchup_1_2.play_n_games(number_of_games)
matchup_1_2.generate_report(f"competition/week_1/{player_1_name}_vs_{player_2_name}.txt")

# MATCHUP 1 and 3
agent_1 = Agent(player_1_name, player_1)
agent_3 = Agent(player_3_name, player_3)
matchup_1_3: Matchup = Matchup(board_dim, 4, agent_1, agent_3, 2, 1)
matchup_1_3.play_n_games(number_of_games)
matchup_1_3.generate_report(f"competition/week_1/{player_1_name}_vs_{player_3_name}.txt")

# # MATCHUP 2 and 3
agent_2 = Agent(player_2_name, player_2)
agent_3 = Agent(player_3_name, player_3)
matchup_2_3: Matchup = Matchup(board_dim, 4, agent_2, agent_3, 2, 1)
matchup_2_3.play_n_games(1000)  # Use different number for this matchup
matchup_2_3.generate_report(f"competition/week_1/{player_2_name}_vs_{player_3_name}.txt")



