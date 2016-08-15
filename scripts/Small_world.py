import axelrod as axl
import networkx as nx
import random
import tqdm
import os

import pandas as pd
import numpy as np

import os.path

from functions import *
from data_structure import *

# parameters
turns = 2
repetitions = 3
ub_tournament_size = 5
ub_seed = 8
num_sample_players = 6
ub_parameter = 3

ordinary_players = [s() for s in axl.strategies]

# titles
experiment = 'watts_strogatz'

# where to export
write_out = '/Users/vince/Desktop/error_{}.h5'.format(experiment)
file_exists = os.path.isfile(write_out)
try:
    os.remove(write_out)
except FileNotFoundError:
    pass

hdf = pd.HDFStore('storage.h5')

tournament_id = 0
for tournament_size in tqdm.tqdm(range(2, ub_tournament_size + 1)):
    for initial_neighborhood_size in range(1, tournament_size):

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
                    G = nx.watts_strogatz_graph(len(players),
                                                initial_neighborhood_size, p)
                    # check for unconnected nodes
                    connections = [len(c) for c in
                                   sorted(nx.connected_components(G), key=len,
                                                                  reverse=True)]

                    if connections and (1 not in connections):
                    # Some description of what is going on.
                        edges = G.edges()

                        tournament_id += 1
                        results = tournament_results(G,
                                                    seed, p, players, turns,
                                                       edges, repetitions,
                                                     tournament_id,
                                                     initial_neighborhood_size)

                        min_itemsize = {'player_name': 100,
                                        'neighbors': 200,
                                        'cliques': 200}

                        hdf.append('d1', results, format='table', data_columns=True,
                                   min_itemsize=min_itemsize)
                        #results = results[cols]

                        #if not file_exists:
                            #results.to_hdf(write_out, '{}'.format(experiment),
                                           #index=False,
                                           #header=True)
                        #else:
                            #results.to_hdf(write_out, '{}'.format(experiment),
                                           #mode='a', index=False,
                                           #header=False)
