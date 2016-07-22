import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

from functions import *
from data_structure import *

# parameters
turns = 200
repetitions = 5
ordinary_players = [s() for s in axl.ordinary_strategies]

# where to export
write_out = '/home/nikoleta/src/jobs/data/Cycle.csv'

results = pd.DataFrame()
for seed in range(0, 1):

    np.random.seed(seed)

    # define the graph
    players = random.sample(ordinary_players, 5)
    for p in range(0, 5) :
        # shuffle the players list
        random.shuffle(players, random.random)

        # Define graph
        G = nx.cycle_graph(len(players))
        # K = nx.newman_watts_strogatz_graph(len(players), 4, 0)

        edges = G.edges()

        filename = '/home/nikoleta/src/jobs/data/Cycle-{}-{}.csv'.format(seed, p)
        # in file name the first number is the seed the second in which
        # shuffle
        results = results.append([tournament_results(G, seed, p, players, turns,
                               edges, repetitions, filename)])

results = results[cols]
results.to_csv(write_out, index=False)