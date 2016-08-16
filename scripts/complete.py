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
experiment = 'round_robin'
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

        # Define graph
        G = nx.complete_graph(len(players))

        edges = G.edges()
        tournament_id += 1
        results = tournament_results(G, tournament_size, num_sample_players,
                                             players, turns, edges, repetitions)

        min_itemsize = {'player_name': 100, 'neighbors': 200}

        hdf.append(experiment, results, format='table', data_columns=True,
                                                      min_itemsize=min_itemsize)
