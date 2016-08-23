import pandas as pd
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from sys import argv

data = pd.read_hdf(argv[1])
title = argv[2]

# fixing index of the data
data.index = range(len(data))

# only for complete
if argv[2] == 'round_robin':
    # for round robin we do not need parameter
    data.drop('parameter', axis=1, inplace=True)
    # and seed for the rr is the tournament size
    data['tournament_size'] = data.seed
    data.drop('seed', axis=1, inplace=True)
else :
    # tournament size for the rest
    data['tournament_size']=data.groupby('tournament_id')['player_name'].transform('count').values

# frequency
data['frequency'] = data.groupby('player_name')['player_name'].transform('count')

# crosstab of players and rank
players_ranking = pd.crosstab(data.player_name, data.ranking)

# wins
wins = pd.DataFrame({'player_name' : list(players_ranking.index),
                               'wins' : players_ranking[0].values})

# ratio
data = pd.merge(data, wins)
data['ratio'] = data.wins/data.frequency

# normalized average score
data['normalized_average_score'] = data.average_score/data.frequency

# cliques by re - creating manually the graph
cliques = []
for i in data.tournament_id.unique() :
    # get the nodes
    players = data.tournament_size[data.tournament_id==i].values[0]
    G = nx.Graph()
    G.add_nodes_from(range(players))

    # get the edges
    edges = []
    for j in data.index[data.tournament_id==i]:
        neighbors = data.neighbors[data.tournament_id==i][j].split("|")
        neighbors = map(int, neighbors)
        edges.append([tuple((data.player_index[data.tournament_id==i][j], k)) for k in neighbors])
    edges = sum(edges, [])
    G.add_edges_from(edges)

    # get the cliques
    nx.find_cliques(G)
    for z in G.nodes() :
        cliques.append(nx.cliques_containing_node(G, z))
# pass it as column
data['cliques'] = cliques

# cliques number
data['num_cliques'] = data.cliques.map(len)

# output what we want
data.to_hdf("/home/nikoleta/src/jobs/data/After-{}.h5".format(title), title)
