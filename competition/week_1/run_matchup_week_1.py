
from competition.week_1.agents import columnator_and_heuritic, weak_1_ncc_play_winning_move
from src.main.connect import Matchup

player_1_name = weak_1_ncc_play_winning_move.get_name()
player_1 = weak_1_ncc_play_winning_move.play
player_2_name = 'heuritic'
player_2 = columnator_and_heuritic.heuritic
player_3_name = 'columnator'
player_3 = columnator_and_heuritic.columnator

# MATCHUP 1 and 2
matchup_1_2: Matchup = Matchup(7, 6, 4, player_1_name, player_2_name, player_1, player_2, 2, 1, 100)
matchup_1_2.play_matchup()
matchup_1_2.generate_report(f"competition/week_1/{player_1_name}_vs_{player_2_name}.txt")

# MATCHUP 1 and 3
matchup_1_3: Matchup = Matchup(7, 6, 4, player_1_name, player_3_name, player_1, player_3, 2, 1, 100)
matchup_1_3.play_matchup()
matchup_1_3.generate_report(f"competition/week_1/{player_1_name}_vs_{player_3_name}.txt")

# # MATCHUP 2 and 3
matchup_2_3: Matchup = Matchup(7, 6, 4, player_2_name, player_3_name, player_2, player_3, 2, 1, 1000)
matchup_2_3.play_matchup()
matchup_2_3.generate_report(f"competition/week_1/{player_2_name}_vs_{player_3_name}.txt")



