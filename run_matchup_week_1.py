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

# MATCHUP 1 and 2
matchup_1_2: ConnectXMatchup = ConnectXMatchup(7, 6, 4, player_1_name, player_2_name, player_1, player_2, 2, 5, 100)
matchup_1_2.play_matchup()
matchup_1_2.generate_report(f"out/{player_1_name}_vs_{player_2_name}.txt")

# MATCHUP 1 and 3
matchup_1_3: ConnectXMatchup = ConnectXMatchup(7, 6, 4, player_1_name, player_3_name, player_1, player_3, 2, 5, 100)
matchup_1_3.play_matchup()
matchup_1_3.generate_report(f"out/{player_1_name}_vs_{player_3_name}.txt")

# MATCHUP 2 and 3
matchup_2_3: ConnectXMatchup = ConnectXMatchup(7, 6, 4, player_2_name, player_3_name, player_2, player_3, 2, 5, 100)
matchup_2_3.play_matchup()
matchup_2_3.generate_report(f"out/{player_2_name}_vs_{player_3_name}.txt")



