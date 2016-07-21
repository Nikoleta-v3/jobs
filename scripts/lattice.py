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
players = random.sample([s() for s in axl.ordinary_strategies], 10)

# where to export
write_out = '/home/nikoleta/src/jobs/data/Lattice.csv'

results = pd.DataFrame()
for seed in range(0, 100):

    np.random.seed(seed)
    p = seed/100
    filename = '/home/nikoleta/src/jobs/data/Lattice-{}.csv'.format(seed)
    # define the graph
    G = nx.newman_watts_strogatz_graph(len(players), 4, p)
    edges = G.edges()

    results = results.append([tournament_results(G, seed, p, players, turns,
                               edges, repetitions, filename)])

results = results[cols]
results.to_csv(write_out, index=False)
