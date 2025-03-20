from src.main.connect import Matchup, ConnectXVisual, Agent, BoardDimension, MetaMatchup, Tournament
import random
import multiprocessing as mp
import os




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
    """
    Play a matchup of 20 games in parallel between two agents and generate a report.
    
    Args:
        first_agent (Agent): The first agent
        second_agent (Agent): The second agent
    """
    print(f"Playing matchup between {first_agent.name} and {second_agent.name}...")
    
    # Create board dimensions and parameters
    board_dim = BoardDimension(7, 6)  # Standard Connect 4 board size
    win_length = 4
    time_limit = 5  # 5 seconds per move
    win_threshold = 10  # 10% threshold for declaring a winner
    
    # Create the matchup
    matchup = Matchup(
        board_dim,
        win_length,
        first_agent,
        second_agent,
        time_limit,
        win_threshold
    )
    
    # Play 20 games in parallel
    # num_processes = mp.cpu_count()
    # matchup.play_n_games_with_parallelism(20, num_processes=num_processes)
    matchup.play_n_games(20)
    
    # Print results to console
    print("\nMatchup Results:")
    print(f"Games played: {matchup.first_player_wins + matchup.second_player_wins + matchup.draws}")
    print(f"{first_agent.name} wins: {matchup.first_player_wins} ({matchup.percentage_first_player_wins:.1f}%)")
    print(f"{second_agent.name} wins: {matchup.second_player_wins} ({matchup.percentage_second_player_wins:.1f}%)")
    print(f"Draws: {matchup.draws} ({matchup.percentage_draws:.1f}%)")
    print(f"Winner: {matchup.winner}")
    
    # Generate report file
    report_dir = "competition/week_2/results"
    os.makedirs(report_dir, exist_ok=True)
    report_path = f"{report_dir}/{first_agent.name}_vs_{second_agent.name}.txt"
    matchup.generate_report(report_path)
    print(f"\nReport saved to: {report_path}")
    
    return matchup




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

