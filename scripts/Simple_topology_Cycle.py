import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

from functions import *
from data_structure import *

# parameters
turns = 200
repetitions = 100
ordinary_players = [s() for s in axl.ordinary_strategies]

# where to export
write_out = '/home/c1569433/src/jobs/data/Cycle/50_Players/Cycle.csv'

results = pd.DataFrame()
for seed in range(0, 50):

    np.random.seed(seed)

    # define the graph
    players = random.sample(ordinary_players, 50)
    for p in range(0, 10) :
        # shuffle the players list
        random.shuffle(players, random.random)

        # Define graph
        G = nx.cycle_graph(len(players))

        edges = G.edges()

        #filename = '/home/c1569433/src/jobs/data/Cycle/5_Players/Cycle-{}-{}.csv'.format(seed, p)
        # in file name the first number is the seed the second in which
        # shuffle
        results = results.append([tournament_results(G, seed, p, players, turns,
                                  edges, repetitions )]) # filename)


        results.to_csv(write_out, mode ='a' , index=False)
