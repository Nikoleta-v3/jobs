import axelrod as axl
import networkx as nx
import random

import pandas as pd
import numpy as np


def neighbors(G, players):
    """
    Returns a list with the neighbors of a player. By neighbors
    we mean the players a player interacts with.
    """
    neighbors = []
    for i in range(len(players)) :
        neighbors.append(G.neighbors(i))
    return neighbors

def neighborhood_size (Neighborhood) :
    """
    Returns the size of the neighborhood of a player.
    """
    neighborhood_size = []
    for i in range(len(Neighborhood)) :
        neighborhood_size.append(len(Neighborhood[i]))
    return neighborhood_size

def normalised_average_neighborhood_score(G, results):
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

def compress_list_of_lists(lst):
    """
    Returns a compressed list of lists
    """
    return ["|".join([str(ele) for ele in l]) for l in lst]

def tournament(G, seed, players,
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
    return tournament.play(progress_bar='/scratch/c1569433/data/{}.h5')

def tournament_results(G, seed, p, players, turns, edges,
                       repetitions, idn=0, initial_neighbourhood_size=2):
    """
    Creates a data frame with parameters of the tournament.

    Parameters
    ----------
    tournament_id: integer
            A number representing the index number of a tournament
    seed : integer
            A seed for the tournament and graph
    player_index : integer
            A players index number
    player_name : character
            The name of the player
    cooperating_ratio : float
            A float number representing the cooperating ratio of the strategy
            for a specific tournament
    degree : integer
            The degree of the graph
    neighbors : list
            A list with the player's neighbors index number
    neighborhood_size: integer
            The size of the neighborhood, should be equal with the degree
    ranking : integer
            The rank of the player
    average_score : float
            The average score achieved by each strategy
    average_neighborhood_score : float
            The average score of the neighbors scores#
    R : integer
            Reward payoff
    P : integer
            Punishment payoff
    T : integer
            Temptation payoff
    S : integer
            Suckers payoff
    connectivity : integer
            Node connectivity of the graph
    clustering : float
            Clustering coefficient for nodes.
    cliques : list
            Cliques that exist in the graph
    initial_neighbourhood_size : integer
            Initial number of neighbors
    """
    # generate the tournament and the results
    results = tournament(G, seed, players, turns, edges,
                         repetitions)

    # parameters
    neighborhood = neighbors(G, results.players)
    nsize = neighborhood_size(neighborhood)
    degree = list(G.degree(G.nodes()).values())
    normalised_av_nscore = normalised_average_neighborhood_score(G, results)
    cliques = Cliques(G)

    # create data frame
    data = pd.DataFrame({'tournament_id' : [idn for _ in results.players],
                         'seed' : seed, 'parameter': p ,
                         'player_index' : G.nodes(),
                         'player_name' : results.players,
                         'cooperating_ratio' : results.cooperating_rating,
                         'degree' : degree ,
                         'neighbors' : compress_list_of_lists(neighborhood),
                         'neighborhood_size' : nsize,
                         'ranking' : results.ranking,
                         'average_score' :
                         [np.median(scores) for scores in results.normalised_scores],
                         'average_neighborhood_score' : normalised_av_nscore,
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
                         'initial_neighbourhood_size': [initial_neighbourhood_size for _ in results.players],
                        })

    return data
