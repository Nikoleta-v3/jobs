import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np
import os.path

from functions import *
from data_structure import *

# parameters
turns = 200
repetitions = 10
ordinary_players = [s() for s in axl.ordinary_strategies]
num_players = 5
# where to export
write_out = '/scratch/c1569433/data/Lattice_{}_players.csv'.format(num_players)
file_exists = os.path.isfile(write_out)

results = pd.DataFrame()
for seed in range(0, 10):

    np.random.seed(seed)

    # define the graph
    players = random.sample(ordinary_players, num_players)
    for p in range(0, 5) :
        # shuffle the players list
        random.shuffle(players, random.random)

        # Define graph
        G = nx.newman_watts_strogatz_graph(len(players), 4, 0)

        edges = G.edges()

        #filename = '/home/c1569433/src/jobs/data/Lattice/5_Players/Lattice-{}-{}.csv'.format(seed, p)
        # in file name the first number is the seed the second in which
        # shuffle

        results = results.append([tournament_results(G, seed, p, players, turns,
                               edges, repetitions)]) #filename

        results = results[cols]

        if not file_exists:
            results.to_csv(write_out, index=False, header=True)
        else :
            results.to_csv(write_out, mode='a',  index=False, header=False)
