from src.main.connect import Matchup, ConnectXVisual, Agent, BoardDimension, MetaMatchup, Tournament
import random




##### THRESHOLD AGENTS #####
from competition.week_2.agents.threshold_week_2 import heuritic, columnator

threshold_columnator: Agent = Agent("columnator", columnator)
threshold_heuritic: Agent = Agent("heuritic", heuritic)




##### WEEK AGENTS #####
def random_move(board, win_length, opponent_name):
    return random.randint(0, board.shape[0] - 1)

from competition.week_2.agents import inquisition, weak_2_ncc_play_winning_move, big_learner
big_learner_instance = big_learner.BIGLEARNER()
big_learner_instance.load_learning_table()
alex: Agent = Agent(big_learner_instance.new_agent_who_dis(), big_learner_instance.play)
nathaniel = Agent(weak_2_ncc_play_winning_move.get_name(), weak_2_ncc_play_winning_move.play)
sam = Agent(inquisition.get_name(), inquisition.play)




def play_one_matchup(first_agent: Agent, second_agent: Agent):
    visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
    visual.play_real_time_game(first_agent.name, second_agent.name, first_agent.play, second_agent.play, 1, 2)





if __name__ == "__main__":
    play_one_matchup(sam, nathaniel)
    # visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
    # visual.play_multiple_real_time_games(nathaniel, threshold_heuritic, 5, 2, 5)


    # ##### Visualizing the game ######
    # # Playing a game manually 
    
    # visual.play_manual_game("X", "O")

    # # Play a game against an agent
    # visual: ConnectXVisual = ConnectXVisual(7, 6, 4, 100, 100)
    # visual.play_manual_against_agent("Human", "AI", agent_first_column, True, 1, 0.2)

    # # Visualize a game between two agents
    # visual = ConnectXVisual(7, 6, 4, 100, 100)
    # visual.play_real_time_game("X", "O", agent_first_column, random_agent_1, 1, 2)

    # Visualize X games between two agents (will alternate the starting player)
    # visual = ConnectXVisual(7, 6, 4, 100, 100)
    # agent_1: Agent = Agent("Agent1", agent_first_column)
    # agent_2: Agent = Agent("Agent2", random_agent_1)
    # visual.play_multiple_real_time_games(agent_1, agent_2, 1, 2, 3)

