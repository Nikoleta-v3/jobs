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

for i in range (2) :
    if i == 0 :
        num_neighbors = '4'
        neighbors = 4
    if i ==1  :
        num_neighbors = '8'
        neighbors = 8

    # Title
    experiment = 'watts_strogatz_graph'

    # where to export
    write_out = '/scratch/c1569433/Desktop/{}_{}.h5'.format(experiment, num_neighbors)
    file_exists = os.path.isfile(write_out)

    results = pd.DataFrame()
    for seed in range(0, 10):

        # set seed
        axl.seed(seed)

        num_players = random.randint(2, 132)
        # define the graph
        players = random.sample(ordinary_players, num_players)

        for parameter in range(0, 101) :

            p = parameter/100
            # Define graph
            G = nx.watts_strogatz_graph(len(players), 8, p)

            edges = G.edges()

            results = results.append([tournament_results(G, seed, p, players, turns,
                                   edges, repetitions)])

            results = results[cols]

            if not file_exists:
                results.to_hdf(write_out, '{}_{}'.format(experiment, num_neighbors),
                               index=False, header=True)
            else :
                results.to_hdf(write_out, '{}_{}'.format(experiment, num_neighbors),
                               mode='a',  index=False, header=False)
