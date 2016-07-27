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
write_out = '/scratch/c1569433/data/Circle_{}_players.csv'.format(num_players)
file_exists = os.path.isfile(write_out)

results = pd.DataFrame()
for seed in range(0, 100):

    # set seed
    axl.seed(seed)

    # define the graph
    players = random.sample(ordinary_players, num_players)

    for p in range(0, 10) :
        # shuffle the players list
        random.shuffle(players)

        # Define graph
        G = nx.newman_watts_strogatz_graph(len(players), 4, 0)

        edges = G.edges()

        results = results.append([tournament_results(G, seed, p, players, turns,
                               edges, repetitions)])

        results = results[cols]

        if not file_exists:
            results.to_csv(write_out, index=False, header=True)
        else :
            results.to_csv(write_out, mode='a',  index=False, header=False)
        
