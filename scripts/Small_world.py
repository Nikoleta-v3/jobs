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
ub_neighborhood_size = 50
ub_seed = 10
num_sample_players = 10
ub_parameter = 10

ordinary_players = [s() for s in axl.strategies]

# TitleS
experiment = 'watts_strogatz'

# where to export
write_out = '/scratch/c1569433/data/{}.h5'.format(experiment)
file_exists = os.path.isfile(write_out)

results = pd.DataFrame()
for neighborhood_size in range(2, ub_neighborhood_size):
    for initial_neighbors in range(1, neighborhood_size):

        # set seed
        axl.seed(neighborhood_size)

        for _ in range (num_sample_players)
            # create players
            players = random.sample(ordinary_players, neighborhood_size)

            for parameter in range(0, ub_parameter) :
                for seed in range(ub_seed) :
                    p = parameter/10

                    axl.seed(seed)
                    # Define graph
                    G = nx.watts_strogatz_graph(len(players),
                                                           initial_neighbors, p)
                    # check for unconnected nodes
                    connections = [len(c) for c in
                                   sorted(nx.connected_components(G), key=len,
                                                                  reverse=True)]


                    if connections and 1 not in connections:

                            edges = G.edges()
                            results = results.append([tournament_results(G,
                                                        seed, p, players, turns,
                                                           edges, repetitions)])
                            results = results[cols]
                            print("game", seed, parameter)
                            if not file_exists:
                                results.to_hdf(write_out, '{}'.format(experiment),
                                               index=False,
                                               header=True)
                            else :
                                results.to_hdf(write_out, '{}'.format(experiment),
                                               mode='a',  index=False,
                                               header=False)
                            success = True
