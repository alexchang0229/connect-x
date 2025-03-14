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




def play_one_meta_matchup(first_agent: Agent, second_agent: Agent):
        # board_dimensions = [BoardDimension(7, 6), BoardDimension(8, 7)]
    board_dimensions = [BoardDimension(7, 6), BoardDimension(7, 6), BoardDimension(7, 6), BoardDimension(7, 6), BoardDimension(7, 6)]
    # win_lengths = [4, 5]
    win_lengths = [4]
    meta_matchup: MetaMatchup = MetaMatchup(
        board_dimensions,
        win_lengths,
        first_agent,
        second_agent,
        turn_time_limit_s=5,
        win_percentage_threshold_for_win=10,
        number_of_games_per_matchup=2
    )
    meta_matchup.play_matchups()
    meta_matchup.generate_report("test.txt")
    print("hello")

##### TOURNAMENT #####
def play_tournament():
    agents = [threshold_heuritic, nathaniel, alex, sam]
    board_dimensions = [
        BoardDimension(7, 6) 
    ]
    win_lengths = [4]
    tournament: Tournament = Tournament(
        board_dimensions,
        win_lengths,
        agents,
        turn_time_limit_s=5,
        win_percentage_threshold_for_win=5,
        number_of_games_per_matchup=10
    )
    tournament.play_tournament("competition/week_2/results")
    tournament.generate_reports_in_dir("competition/week_2/results")






if __name__ == "__main__":
##### Generating the matchup ######
    # play_tournament()
    # play_one_meta_matchup()


    play_one_meta_matchup(sam, threshold_heuritic)
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

