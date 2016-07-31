import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

import csv

# parameters
turns = 200
repetitions = 100
players = [s() for s in axl.ordinary_strategies]

# where to export
write_out = '/scratch/c1569433/data/Players.csv'

tournament = axl.Tournament(players, turns=turns, repetitions=repetitions)

results = tournament.play()

players_list = pd.DataFrame({ 'Names' : players,
                              'Cooperation' : results.cooperating_rating})

players_list.to_csv(write_out,index=False,)
