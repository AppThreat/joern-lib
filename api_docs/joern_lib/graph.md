Module joern_lib.graph
======================

Functions
---------

    
`convert_dot(data)`
:   Function to convert dot data into graph

    
`diff(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   Function to compute the difference between two graphs

    
`diff_graph(first_graph, second_graph, include_common=False, as_dict=False, as_dot=False)`
:   Function to compute the difference between two graphs and optionally convert the result to dict or dot format

    
`ged(first_graph, second_graph, timeout=5, upper_bound=500)`
:   Function to compute the difference based on graph edit distance algorithm

    
`gep(first_graph, second_graph, upper_bound=500)`
:   Function to compute the difference based on optimal edit path algorithm

    
`hash(G, subgraph=False, edge_attr='label', node_attr='label', iterations=3, digest_size=16)`
:   Function to compute the hashes for a graph using Weisfeiler Lehman hashing algorithm

    
`is_similar(M1, M2, upper_bound=500, timeout=5)`
:   Function to check if two graphs are similar. To simplify the problem, first the raw graph difference is computed to check if the graphs are the same.
    If not graph edit distance is computed with a fixed timeout to help answer the question

    
`node_match_fn(n1, n2)`
:   

    
`summarize(G, as_dict=False, as_dot=False)`
:   Function to summarize the graph based on node labels

    
`write_dot(G, path)`
:   Function to export graph as dot