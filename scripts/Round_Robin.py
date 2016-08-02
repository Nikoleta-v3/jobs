import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

import os.path

# parameters
turns = 200
repetitions = 10
ordinary_players = [s() for s in axl.strategies]
num_players = 5

# where to export
write_out = '/scratch/c1569433/data/Round_Robin_{}.csv'.format(num_players)
file_exists = os.path.isfile(write_out)
winners= []
norm_scores=[]
score = []
average_score= []
for seed in range(0, 100):

    # set seed
    axl.seed(seed)


    players = random.sample(ordinary_players, num_players)

    tournament = axl.Tournament(players, turns=turns, repetitions=repetitions)
    results = tournament.play()

    data = pd.DataFrame({'players_list' :
                          [players for _ in results.players],
                         'seed' : seed,
                         'scores' : results.scores,
                         'normalised_scores' :
                          results.normalised_scores,
                         'average_score' :
                          [np.median(scores) for scores in results.normalised_scores],
                          'winners' : results.ranked_names
                        })

    if not file_exists:
        data.to_csv(write_out, index=False, header=True)
    else :
        data.to_csv(write_out, mode='a',  index=False, header=False)
