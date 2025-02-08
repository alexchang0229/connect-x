import unittest
import pytest
import tkinter as tk
import random

from main.connect import GameState, ConnectXMatch, ConnectXMatchWithAgents, ConnectXMatchup, ConnectXVisual

from competition.week_1 import weak_1_ncc_play_winning_move, columnator_and_heuritic

player_1_name = weak_1_ncc_play_winning_move.get_name()
player_1 = weak_1_ncc_play_winning_move.play
player_2_name = 'heuritic'
player_2 = columnator_and_heuritic.heuritic
player_3_name = 'columnator'
player_3 = columnator_and_heuritic.columnator


# 5 games between player 1 and player 2
for i in range(2):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game(player_1_name, player_2_name, player_1, player_2, 1)
    visual.play_real_time_game(player_2_name, player_1_name, player_2, player_1, 1)

# 5 games between player 1 and player 3
for i in range(5):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game(player_1_name, player_3_name, player_1, player_3, 1)
    visual.play_real_time_game(player_3_name, player_1_name, player_3, player_1, 1)

# 5 games between player 2 and player 3
player_2_name = 'heuritic'
player_3_name = 'columnator'
for i in range(5):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game(player_2_name, player_3_name, player_2, player_3, 1)
    visual.play_real_time_game(player_3_name, player_2_name, player_3, player_2, 1)




