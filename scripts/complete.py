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
ub_tournament_size = 50
num_sample_players = 10

ordinary_players = [s() for s in axl.strategies]

# titles
experiment = 'round_robin'

# where to export
write_out = '/scratch/c1569433/data/{}.h5'.format(experiment)
file_exists = os.path.isfile(write_out)

results = pd.DataFrame()
for tournament_size in range(2, ub_tournament_size):

    # set seed
    axl.seed(tournament_size)

    for sample_players in range (num_sample_players) :
        # create players
        axl.seed(sample_players)
        players = random.sample(ordinary_players, tournament_size)

        # Define graph
        G = nx.complete_graph(len(players))

        edges = G.edges()
        results = results.append([tournament_results(G, tournament_size,
                                             num_sample_players, players, turns,
                                                           edges, repetitions)])

        results = results[cols]

        if not file_exists:
            results.to_hdf(write_out, '{}'.format(experiment), index=False,
                                                                    header=True)
        else :
            results.to_hdf(write_out, '{}'.format(experiment), mode='a',
                                                      index=False, header=False)
