import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

import csv

# parameters
turns = 200
repetitions = 100
ordinary_players = [s() for s in axl.ordinary_strategies]
num_players = 5

# where to export
write_out = '/scratch/c1569433/data/Round_Robin_{}_players.csv'.format(num_players)

winners= []
for seed in range(0, 100):

    # set seed
    axl.seed(seed)


    players = random.sample(ordinary_players, num_players)

    tournament = axl.Tournament(players, turns=turns, repetitions=repetitions)
    results = tournament.play()
    winners.append(results.ranked_names)

wins = pd.DataFrame(winners)
wins.to_csv(write_out)
