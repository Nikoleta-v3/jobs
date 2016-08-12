import pandas as pd
import numpy as np

from sys import argv

data = pd.read_hdf(argv[1])
title = argv[2]

# fixing index of the data
data.index = range(len(data))

# fixing the players list
players_list= []
for i in range(len(data)) :
    x = data.players_list[i][2:].split("],")
    players_list.append(x[0])
data['players_list'] = players_list

# fixing the players name
player_name = []
for i in range(len(data)):
    x = data.players_list[i].split(", ")
    player_name.append(x[data.player_index[i]])
data.player_name = player_name

# count tournaments
tournament = []
count = 0
for i in range(len(data)):
    if data.ranking[i] == 0 :
        count = count +1
    else : count = count

    tournament.append(count)
data['number_of_tournaments'] = tournament

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

# crosstab of players and cooperating ratio
cooperation = pd.crosstab(data.player_name, data.cooperating_ratio)

# classification based on cooperating ratio
classification = []
for i in range(len(data)):
    if data.cooperating_ratio[i] <= 0.2 :
        classification.append('low')
    if data.cooperating_ratio[i] > 0.2 and data.cooperating_ratio[i] <= 0.4 :
         classification.append('weak')
    if data.cooperating_ratio[i] > 0.4 and data.cooperating_ratio[i] <= 0.6 :
         classification.append('mid')
    if data.cooperating_ratio[i] > 0.6 and data.cooperating_ratio[i] <= 0.8 :
         classification.append('moderate')
    if data.cooperating_ratio[i] > 0.8 and data.cooperating_ratio[i] <= 1 :
         classification.append('high')
data['classification'] = classification

summary = data.describe()

# output what we want
data.to_hdf("/scratch/c1569433/data/ratio-{}.h5".format(title), title)
summary.to_csv("/scratch/c1569433/data/summary-{}.csv".format(title))
