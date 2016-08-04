import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np

def Neighbors(G, players):
    """
    Returns a list with the neighbors of a player. By neighbors
    we mean the players a player interacts with.
    """
    Neighbors = []
    for i in range(len(players)) :
        Neighbors.append(tuple(players[j] for j in G.neighbors(i)))
    return Neighbors

def Neighborhood_size (Neighborhood) :
    """
    Returns the size of the neighborhood of a player.
    """
    Neighborhood_size = []
    for i in range(len(Neighborhood)) :
        Neighborhood_size.append(len(Neighborhood[i]))
    return Neighborhood_size

def Neighbors_Scores(G, results, players):
    """
    Returns a list with the scores of the
    neighbors.
    """
    return [[results.scores[j] for j in G.neighbors(i)]
            for i, pl in enumerate(players)]

def Neighbors_Normalized_Scores(G, results, players):
    """
    Returns a list with the normalized scores of the
    neighbors.
    """
    return [[results.normalised_scores[j] for j in G.neighbors(i)]
            for i, pl in enumerate(players)]

def Average_Neighborhood_Score(G, results) :
    """
    Returns the average score of the sum of the neighbors
    scores. Thus, the average score of the neighborhood.
    """
    av_score = []
    temp = [[j for m in G.neighbors(k)
             for j in results.scores[m]] for k in G.nodes()]
    for i in G.nodes() :
        av_score.append(np.mean(temp[i]))
    return av_score

def Normalised_Average_Neighborhood_Score(G, results):
    """
    Returns the average score of the sum of the neighbors
    scores. Thus, the average score of the neighborhood.
    """
    av_score = []
    temp = [[j for m in G.neighbors(k)
             for j in results.normalised_scores[m]] for k in G.nodes()]
    for i in G.nodes() :
        av_score.append(np.mean(temp[i]))
    return av_score

def Cliques(G) :
    """
    Return a list of cliques the player belongs to
    """
    nx.find_cliques(G)
    cliques = []
    for i in G.nodes() :
        cliques.append(nx.cliques_containing_node(G, i))
    return cliques

def touranment(G, seed, players,
               turns, edges, repetitions): # filename)
    """
    Run a spatial tournament with a topology of any given
    graph. Return the results.
    """
    # set seed the tournament.
    random.seed(seed)
    np.random.seed(seed)
    edges = G.edges()

    # create tournament
    tournament = axl.SpatialTournament(players = players,
                                       edges= edges,
                                       turns = turns,
                                       repetitions= repetitions)

    # play the tournament. Return the results.
    return tournament.play()

def tournament_results(G, seed, p, players, turns, edges, repetitions):
    """
    Creates a data frame with parameters of the tournament.

    Parameters
    ----------
    players_list : list
            A list with the players participating in the tournament
    seed : integer
            A seed for the tournament and graph
    player_index : integer
            A players index number
    player_name : character
            The name of the player
    degree : integer
            THe degree of the graph
    neighbors : list
            A list with the player's neighbors index number
    neighborhood_size: integer
            The size of the neighborhood, should be eqaul with the degree

    """
    # generate the tournament and the results
    results = touranment(G, seed, players, turns, edges,
                         repetitions) # filename)

    # parameters
    neighborhood = Neighbors(G, players)
    nsize = Neighborhood_size(neighborhood)
    degree = list(G.degree(G.nodes()).values())
    nscores = Neighbors_Scores(G, results, players)
    normalised_nscore = Neighbors_Normalized_Scores(G, results, players)
    normalised_av_nscore = Normalised_Average_Neighborhood_Score(G, results)
    av_nscores = Average_Neighborhood_Score(G, results)
    cliques = Cliques(G)

    # create data frame
    data = pd.DataFrame({'players_list' :
                          str([players for _ in results.players]),
                         'seed' : seed, 'parameter': p ,
                         'player_index' : G.nodes(),
                         'player_name' : str(results.players),
                         'cooperating_ratio' : results.cooperating_rating,
                         'degree' : degree ,
                         'neighbors' : str(neighborhood),
                         'neighborhood_size' : nsize,
                         'ranking' : results.ranking,
                         'scores' : str(results.scores),
                         'normalised_scores' :
                          str(results.normalised_scores),
                         'average_score' :
                          [np.median(scores) for scores in results.normalised_scores],
                         'neighbors_scores' : str(nscores),
                         'normalised_neighbors_score' : normalised_nscore,
                         'normalised_average_neighboorhood_score' :
                          normalised_av_nscore,
                         'R' :
                          [list(results.game.RPST())[0] for _ in results.players],
                         'P' :
                          [list(results.game.RPST())[1] for _ in results.players],
                         'S' :
                          [list(results.game.RPST())[2] for _ in results.players],
                         'T' :
                          [list(results.game.RPST())[3] for _ in results.players],
                         'connectivity' : nx.node_connectivity(G),
                         'clustering' : nx.average_clustering(G),
                         'cliques' : str(cliques)
                        })

    return data
