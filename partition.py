"""
partition.py

Geometry of Redistricting Conference 2017-10-14..15 Hackathon

Enumerate all possible partitions of a small map into districts,
to compare results with randomized district sampling algorithms.
"""

from __future__ import division     # for Python 2.7


import networkx as nx


def calc_limits(graph, num_parts, max_ratio):
    """Estimate min and max weights for partitioning graph into num_parts.
        
        Node weight of each subgraph may differ from the average by
            no more than a factor of max_ratio.
        
        graph: networkx.Graph
        num_parts: int
        max_ratio: float
        
        Returns: (min_weight, max_weight)
    """
    nodes = graph.nodes(data='weight')          # sequence of (id, weight)
    weights = [weight for id, weight in nodes]
    total_weight = sum(weights)                 # weight of all nodes
    
    avg_weight = total_weight / num_parts   # average subgraph weight
    max_weight = avg_weight * max_ratio     # largest allowed subgraph weight
    min_weight = avg_weight / max_ratio     # smallest allowed subgraph weight
    return (min_weight, max_weight)


def all_partitions(graph, limits):
    """Enumerate all partitions of graph into subgraphs within weight limits.
        
        graph: networkx.Graph
        limits: (min_weight, max_weight)
        
        Returns: 
            list of partitions, each partition a list of subgraphs,
            each subgraph a list of node
    """
    partitions = []
    
    # Find node with highest weight
    nodes = graph.nodes(data='weight')      # iterator of (id, weight)
    weights = [weight for id, weight in nodes]
    highest_weight = max(weights)
    node_index = weights.index(highest_weight)
    heaviest = list(nodes)[node_index][0]    # id of node with highest weight
    
    # Find all subgraphs containing heaviest node, within weight limits
    subgraphs = accrete(graph,
                        subgraph={heaviest},
                        subgraph_weight=highest_weight,
                        ignore={heaviest},
                        limits=limits)
    
    for subgraph in subgraphs:
        ### Check if subgraph splits graph into disconnected parts?
        ###     If so, check parts for min_weight, 
        ###         discard subgraph if any are underweight.
        
        remainder = graph.copy()
        remainder.remove_nodes_from(subgraph)
        if len(remainder) == 0:             # empty
            partitions.append([subgraph])   # add a 1-part partition
        else:
            subpartitions = all_partitions(remainder, limits)
            # add subgraph to each subpartition
            for subpartition in subpartitions:
                partitions.append(subpartition + [subgraph])
    
    return partitions 


def accrete(graph, subgraph, subgraph_weight, ignore, limits):
    """Find all subgraphs of graph which contain subgraph, within limits.
        
        Subgraphs must have weight (sum of node weights) within limits.
        Ignore any nodes in ignore.
        
        graph: networkx.Graph
        subgraph: set of node
        ignore: set of node
        limits: (min_weight, max_weight)
        
        Returns: list of subgraphs, each a set of node
    """
    min_weight, max_weight = limits
    subgraphs = []
    
    # find all neighbors of subgraph, excluding nodes in ignore
    ### reuse this?
    nbrs = set()
    for node_id in subgraph:
        nbrs |= set(graph[node_id]) - ignore
    
    ### use neighbors of forward node only?
    # Try adding each neighbor to subgraph
    for nbr in nbrs:
        subgraph_weight += graph.nodes[nbr]['weight']
        if subgraph_weight > max_weight:
            ignore.add(nbr)  # nbr too heavy to add to subgraph, skip it later
        else:
            new_subgraph = subgraph | {nbr}
            if subgraph_weight >= min_weight:
                subgraphs.append(new_subgraph)
            subgraphs += accrete(graph, 
                                 new_subgraph,
                                 subgraph_weight,
                                 ignore | {nbr},
                                 limits)
    return subgraphs


if __name__ == "__main__":
    # parseargs: graph_filename, num_parts, max_ratio
    ## ...
    num_parts = 3
    max_ratio = 1.1
    
    # read graph from file given by graph_filename
    ## ...
    
    limits = calc_limits(graph, num_parts, max_ratio)
    partitions = all_partitions(graph, limits)
    # display partitions or write to file


# test data
d = {0: {'weight': 8.0}, 1: {'weight': 15.0}, 2: {'weight': 0.2}, 
     3: {'weight': 6.2}, 4: {'weight': 4.4}, 5: {'weight': 0}}
dt = [(0, {'weight': 8.0}), (1, {'weight': 15.0}), (2, {'weight': 0.2}),
      (3, {'weight': 6.2}), (4, {'weight': 4.4}), (5, {'weight': 0})]
g = nx.Graph()
g.add_nodes_from(dt)
e = [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)]
g.add_edges_from(e)
    
    
    