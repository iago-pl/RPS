import matplotlib.pyplot as plt
import numpy as np

from rps_game import GameResult, play_round
from agents import RPS_AGENTS
from rps_rules import VICTORY_RULES as RPS_VICTORY_RULES, LOSS_RULES as RPS_LOSS_RULES

GAMES = 10000

def play_matches(agent_action, computer_action, victory_rules, loss_rules):
    results = []
    records = []
    for i in range(GAMES):
        (a,b, result) = play_round(agent_action, computer_action, victory_rules, loss_rules, records)
        records.append((a,b, result))
        results.append(result)
    
    return results

def get_stats(results):

    victories = results.count(GameResult.Victory)
    lost = results.count(GameResult.Loss)
    tie = results.count(GameResult.Tie)

    return (victories, lost, tie)

def get_percentages(stats):
    (victories, lost, tie)  = stats
    return (victories / GAMES, lost / GAMES, tie / GAMES)


def test_agents(agent_action, computer_action, victory_rules, loss_rules):
    results = play_matches(agent_action, computer_action, victory_rules, loss_rules)
    (victories, lost, ties) = get_stats(results)
    (victories_perc, lost_perc, ties_perc) = get_percentages((victories, lost, ties))
    print(f"Agent { agent_action.__name__} has {victories} victories, {ties} ties and {lost} lost against {computer_action.__name__}")
    print(f"With {victories_perc * 100}% winrate")
    return (victories, lost, ties)


def match_agents(agents, victory_rules, loss_rules): 
    matches = {}
    for a in agents:
        matches[a] = {}
        for b in agents:
            matches[a][b] = {}
            (matches[a][b][GameResult.Victory], matches[a][b][GameResult.Loss], matches[a][b][GameResult.Tie]) = test_agents(agents[a], agents[b], victory_rules, loss_rules)
    
    return matches

def run(agents, victory_rules, loss_rules):
    matches = match_agents(agents, victory_rules, loss_rules)

    display_winrate(matches)
    display_stacked_bar(matches)

def sum_data(matches, key):
    return [sum(matches[a][b][key] / (GAMES * len(matches)) for b in matches[a]) for a in matches]


def display_stacked_bar(matches):
    agents = [a for a in matches]
    victories = sum_data(matches, GameResult.Victory)
    lost = sum_data(matches, GameResult.Loss)
    ties = sum_data(matches, GameResult.Tie)

    fig, ax = plt.subplots()

    ax.bar(agents, victories, color = "forestgreen")
    ax.bar(agents, ties, bottom = victories, color = "khaki")
    ax.bar(agents, lost, bottom = np.add(victories, ties), color = "lightcoral")

    plt.show()



def display_winrate(matches):
    agents = [a for a in matches]
    wins = sum_data(matches, GameResult.Victory)

    y_pos = np.arange(len(wins))

    plt.bar(y_pos, wins, color = [plt.cm.viridis(sum(ord(c) for c in agent) % 256) for agent in agents])

    plt.xticks(y_pos, agents)

    plt.show()

# def display_stacked_bar(matches):
#     print(matches)


run(RPS_AGENTS, RPS_VICTORY_RULES, RPS_LOSS_RULES)