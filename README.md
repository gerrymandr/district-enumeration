# district-enumeration
Python module to enumerate all partitions of a small graph for a redistricting demo.

partitions(graph, num_parts, max_ratio):
> Enumerate all partitions of (small) graph into num_parts such that the
> total node weight of each subgraph differs from the average by
> no more than a factor of max_ratio.
