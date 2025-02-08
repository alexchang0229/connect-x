import unittest
import pytest
import tkinter as tk
import random

from main.connect import GameState, ConnectXMatch, ConnectXMatchWithAgents, ConnectXMatchup, ConnectXVisual

def get_name_random_agent_1():
    return "Random Agent 1"
def random_agent_1(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def get_name_random_agent_2():
    return "Random Agent 2"
def random_agent_2(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

def get_name_random_agent_3():
    return "Random Agent 3"
def random_agent_3(board, win_length):
    # Random agent that picks a random column
    return random.randint(0, board.shape[0] - 1)

player_1_name = get_name_random_agent_1()
player_1 = random_agent_1
player_2_name = get_name_random_agent_2()
player_2 = random_agent_2
player_3_name = get_name_random_agent_3()
player_3 = random_agent_3



# 5 games between player 1 and player 2
for i in range(5):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game("X", "O", player_1, player_2, 1)

# 5 games between player 1 and player 3
for i in range(5):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game("X", "O", player_1, player_3, 1)

# 5 games between player 2 and player 3
for i in range(5):
    visual = ConnectXVisual(7, 6, 4)
    visual.play_real_time_game("X", "O", player_2, player_3, 1)




