import axelrod as axl
import networkx as nx
import random
import tqdm
import os

import pandas as pd
import numpy as np

import os.path

from functions import *

# parameters
turns = 200
repetitions = 10
ub_tournament_size = 50
ub_seed = 10
num_sample_players = 10
ub_parameter = 10

ordinary_players = [s() for s in axl.strategies]

# titles
experiment = 'binomial'
# create store
hdf = pd.HDFStore('/scratch/c1569433/data/{}.h5'.format(experiment))

tournament_id = 0
for tournament_size in tqdm.tqdm(range(2, ub_tournament_size + 1)):

        # set seed
        axl.seed(tournament_size)

        for sample_players in range (num_sample_players) :
            # create players
            axl.seed(sample_players)
            players = random.sample(ordinary_players, tournament_size)

            for parameter in range(1, ub_parameter + 1) :

                p = parameter/(ub_parameter)
                for seed in range(ub_seed) :

                    axl.seed(seed)
                    # Define graph
                    G = nx.binomial_graph(len(players), p)

                    # check for connected nodes
                    connections = [len(c) for c in
                                   sorted(nx.connected_components(G), key=len,
                                                                  reverse=True)]

                    if connections and (1 not in connections):
                    # if connections is empty, or equal to 1, it means
                    # at least on node is disconnected. Thus, skip this
                    # tournament and generate next
                        edges = G.edges()

                        tournament_id += 1
                        results = tournament_results(G, seed, p, players, turns,
                                                             edges, repetitions,
                                                                  tournament_id,
                                                                              0)

                        min_itemsize = {'player_name': 100, 'neighbors': 200}

                        hdf.append(experiment, results, format='table', data_columns=True,
                                   min_itemsize=min_itemsize)
